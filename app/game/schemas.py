from marshmallow import Schema, fields, post_load

from app.models import Game


class GameSchema(Schema):
    """
    Schema for game object serialization, deserialization.
    """
    id = fields.Str()
    creator_id = fields.Integer()
    opponent_id = fields.Integer()
    last_move_user_id = fields.Integer()
    latest_game_board = fields.Str()
    is_finished = fields.Boolean()
    winner_id = fields.Integer()

    @post_load
    def make_game(self, data, **kwargs):
        return Game(**data)
