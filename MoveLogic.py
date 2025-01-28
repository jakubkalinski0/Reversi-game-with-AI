from typing import List, Tuple

from Board import Board

class MoveLogic:
    DIRECTIONS = [
        (-1, 0), (1, 0),        # Vertical
        (0, -1), (0, 1),        # Horizontal
        (-1, -1), (-1, 1),      # Diagonal Up
        (1, -1), (1, 1)         # Diagonal Down
    ]

    @staticmethod
    def is_move_legal(board: Board, row: int, column: int, color: str) -> bool:
        if row < 0 or row >= board.size or column < 0 or column >= board.size:
            return False
        if board.get_cell(row, column) != None:  # Cell must be empty
            return False

        opponent = "W" if color == "B" else "B"


        for direction_row, direction_column in MoveLogic.DIRECTIONS:
            r, c = row + direction_row, column + direction_column
            found_opponent = False

            # Look in a direction
            while 0 <= r < board.size and 0 <= c < board.size:
                cell = board.get_cell(r, c)
                if cell == None:
                    break
                elif cell.get_color() == opponent:
                    found_opponent = True
                elif cell.get_color() == color and found_opponent:
                    return True
                else:
                    break
                r, c = r + direction_row, c + direction_column

        return False

    @staticmethod
    def get_flipped_pieces(board: Board, row: int, column: int, color: str) -> List[Tuple[int, int]]:
        flipped_pieces = []
        opponent = "W" if color == "B" else "B"

        for direction_row, direction_column in MoveLogic.DIRECTIONS:
            r, c = row + direction_row, column + direction_column
            temp_flipped = []

            # Look in a direction
            while 0 <= r < board.size and 0 <= c < board.size:
                cell = board.get_cell(r, c)
                if cell == None:
                    break
                if cell.get_color() == opponent:
                    temp_flipped.append((r, c))
                elif cell.get_color() == color:
                    flipped_pieces.extend(temp_flipped)
                    break
                else:
                    break
                r, c = r + direction_row, c + direction_column

        return flipped_pieces

    @staticmethod
    def get_legal_moves(board: Board, color: str) -> List[Tuple[int, int]]:
        legal_moves = []
        for row in range(board.size):
            for col in range(board.size):
                if MoveLogic.is_move_legal(board, row, col, color):
                    legal_moves.append((row, col))
        return legal_moves
