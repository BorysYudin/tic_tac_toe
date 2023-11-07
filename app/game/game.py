from enum import Enum
from itertools import chain


class GameStatus(Enum):
    """
    Enum with game statuses.
    WIN in case game is finished and there is a winner.
    DRAW in case game is finished but there is no winner.
    IN_PROGRESS in case came is not finished yet.
    """
    WIN = 1
    DRAW = 2
    IN_PROGRESS = 3


def _is_line_symbols_the_same(line):
    """
    Check if all symbols of the line match and they are not default empty values.
    :param line: tuple of symbols
    :return: boolean, True is symbols match, False in other case
    """
    return line[0] == line[1] == line[2] != ''


def _flatten_matrix(matrix):
    """
    Flatten list of lists to single list.
    :param matrix: list of lists
    :return: flattened list
    """
    return list(chain.from_iterable(matrix))


def get_game_status(board):
    """
    Get the status of the game board. Check all rows, columns and diagonals to specify if the game is finished and there
    is a winner, game is finished and there is draw or if game is still in progress.
    :param board: matrix of board fields
    :return: enum of game status
    """
    lines = [
        # Diagonals of the board
        (board[0][0], board[1][1], board[2][2]),
        (board[0][2], board[1][1], board[2][0]),

        # Rows of the board
        (board[0][0], board[0][1], board[0][2]),
        (board[1][0], board[1][1], board[1][2]),
        (board[2][0], board[2][1], board[2][2]),

        # Columns of the board
        (board[0][0], board[1][0], board[2][0]),
        (board[0][1], board[1][1], board[2][1]),
        (board[0][2], board[1][2], board[2][2]),
    ]

    for line in lines:
        # Check all rows, columns and diagonals for all matching symbols. If all symbols match and not default empty
        # symbols then there is a winner in the game
        if _is_line_symbols_the_same(line):
            return GameStatus.WIN

    # If there is no winner in the game and there are still empty fields on the board then game is still in progress
    if any([item == '' for item in _flatten_matrix(board)]):
        return GameStatus.IN_PROGRESS

    # If there is no winner in the game and game is not in progress then there is a draw.
    return GameStatus.DRAW
