from Board import Board
from MoveLogic import MoveLogic

class GameLogic:
    @staticmethod
    def apply_move(board: Board, row: int, column: int, color: str):
        board.set_cell(row, column, color)
        flipped = MoveLogic.get_flipped_pieces(board, row, column, color)
        for r, c in flipped:
            board.get_cell(r, c).flip()