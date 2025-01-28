"""
This module defines the `GameLogic` class, which manages the core mechanics of the Reversi game.

The `GameLogic` class is responsible for applying moves to the game board, flipping opponent pieces as needed, 
and interacting with the `Board` and `MoveLogic` modules to enforce game rules.
"""

from Board import Board
from MoveLogic import MoveLogic

class GameLogic:
    """
    Implements the core game mechanics for Reversi.

    Methods:
        apply_move(board, row, column, color): Places a piece on the board, flips opponent pieces, and updates the board state.
    """

    @staticmethod
    def apply_move(board: Board, row: int, column: int, color: str):
        """
        Applies a move to the game board by placing a piece and flipping opponent pieces as per the rules.

        Args:
            board (Board): The game board where the move is applied.
            row (int): The row index where the piece is placed.
            column (int): The column index where the piece is placed.
            color (str): The color of the piece being placed ('W' for white, 'B' for black).

        Actions:
            - Places the specified piece on the board.
            - Calculates which opponent pieces are flipped as a result of the move using `MoveLogic`.
            - Flips the relevant pieces on the board.
        """
        # Place the piece on the specified cell
        board.set_cell(row, column, color)

        # Determine which opponent pieces to flip
        flipped = MoveLogic.get_flipped_pieces(board, row, column, color)

        # Flip the determined pieces
        for r, c in flipped:
            board.get_cell(r, c).flip()