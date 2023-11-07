import json
import uuid

from flask import request

from flask_login import login_required, current_user

from app.game import bp
from app.extensions import db
from .schemas import GameSchema
from .game import get_game_status, GameStatus
from app.models import Game

WIN_RATE = 3
DRAW_RATE = 2
LOSE_RATE = 1


@bp.route('/games/create', methods=['POST'])
@login_required
def create_game():
    """
    Endpoint for creating a new game for two players.
    :return: tuple with status message and status code, or created game details with status code
    """
    data = request.get_json()
    # We create a new game with unique uuid and two players: creator (current user) and opponent. By default a new empty
    # board is created.
    new_game = Game(
        id=uuid.uuid4(),
        creator_id=current_user.id,
        opponent_id=data['opponent_id'],
        latest_game_board=json.dumps([['', '', ''], ['', '', ''], ['', '', '']])
    )
    db.session.add(new_game)
    db.session.flush()

    if not new_game.opponent_id:
        return {'msg': 'No opponent id specified.'}, 400

    if new_game.creator_id == new_game.opponent_id:
        return {'msg': 'Creator and opponent can\'t be the same.'}, 400

    db.session.commit()

    return GameSchema().dump(new_game), 200


@bp.route('/games/<game_id>')
@login_required
def get_game(game_id):
    """
    Get game details with the latest board.
    :param game_id: uuid of a game
    :return: game details and status code
    """
    game = Game.query.get(uuid.UUID(game_id))
    return GameSchema().dump(game), 200


def _update_users_rates(game_status, game):
    """
    Update game creator and opponent users rates depending on game results. If one of the user is a winner then it's
    user rate is increased by 3 points, if there is a draw in the game user rate is increased by 2 points, if user is a
    looser then it's user rate is increased by 1 point.
    :param game_status: enum of game status: WIN, DRAW, IN_PROGRESS
    :param game:
    :return:
    """
    if game_status == GameStatus.WIN:
        # If game is finished and there is a winner, then the winner is the user that made the last move.
        game.winner_id = current_user.id
        game.is_finished = True
        # Here and further we update user rate by updating `user_rate`.rate field and increasing it by some points.
        current_user.user_rate.rate += WIN_RATE

        # Here we update opponent user rate by checking user id that is not equal to current user id.
        if game.creator_id == current_user.id:
            game.opponent.user_rate.rate += LOSE_RATE
        else:
            game.cretor.user_rate.rate += LOSE_RATE
    elif game_status == GameStatus.DRAW:
        # Here we update both users rate in case the game finished with DRAW.
        game.is_finished = True
        game.cretor.user_rate.rate += DRAW_RATE
        game.opponent.user_rate.rate += DRAW_RATE


@bp.route('/games/<game_id>/make_a_turn', methods=['POST'])
@login_required
def make_a_turn(game_id):
    data = request.get_json()
    game = Game.query.get(uuid.UUID(game_id))

    if game.is_finished:
        return {'msg': 'This game already finished.'}, 400

    if current_user.id not in [game.creator_id, game.opponent_id]:
        return {'msg': 'Current user not belongs to this game.'}, 400

    if current_user.id == game.last_move_user_id:
        return {'msg': 'Same user can\'t make two moves in a row.'}, 400

    if not game.last_move_user_id and game.creator_id != current_user.id:
        return {'msg': 'First move should be done by game cretor.'}, 400

    # Game creator should make the first move and he's symbol is always `x`. Opponents symbol is always `o`.
    move_symbol = 'x' if current_user.id == game.creator_id else 'o'
    board = json.loads(game.latest_game_board)

    if not 0 <= data['x'] <= 2 and not 0 <= data['y'] <= 2:
        return {'msg': 'Move should be in range 0 to 2'}, 400

    if not board[data['x']][data['y']] == '':
        return {'msg': f'{data["x"]}:{data["y"]} field already filled.'}, 400

    # Here we make a move on a board
    board[data['x']][data['y']] = move_symbol

    # On each move we check if game is finished or still in progress
    game_status = get_game_status(board)

    # In case the game is finished we update users rates
    _update_users_rates(game_status, game)

    game.latest_game_board = json.dumps(board)
    game.last_move_user_id = current_user.id
    db.session.add(game)
    db.session.commit()

    return GameSchema().dump(game), 200
