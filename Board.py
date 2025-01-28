"""
This module defines the `Board` class, which represents the game board for a Reversi game.
The `Board` class handles the grid structure, initialization of the game state, and provides methods for interacting
with the board's state.
"""

from Checker import Checker


class Board:
    """
    Represents the game board for a Reversi game.

    Attributes:
        size (int): The size of the game board (default is 8x8).
        grid (list[list[None or Checker]]): A 2D list representing the board's cells.
            Each cell can be either None (empty) or a `Checker` object representing a piece on the board.

    Methods:
        initialize(): Sets up the board with the initial configuration of pieces.
        get_cell(row, column): Returns the contents of a specific cell (None or a Checker).
        set_cell(row, column, color): Places a piece of the specified color at the given position.
        is_full(): Checks whether the board is completely filled with pieces.
        reset(): Resets the board to the initial state.
    """

    def __init__(self, size: int = 8):
        """
        Initializes a new game board.

        Args:
            size (int): The size of the board. Default is 8, creating an 8x8 board.
        """
        self.size = size
        # Create a 2D grid initialized with None to represent empty cells
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.initialize()

    def initialize(self):
        """
        Sets up the board with the initial configuration of pieces for a standard Reversi game.
        White ('W') pieces are placed at the center positions (mid-1, mid-1) and (mid, mid),
        while Black ('B') pieces are placed at (mid-1, mid) and (mid, mid-1).
        """
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = Checker((mid - 1, mid - 1), "W")
        self.grid[mid][mid] = Checker((mid, mid), "W")
        self.grid[mid - 1][mid] = Checker((mid - 1, mid), "B")
        self.grid[mid][mid - 1] = Checker((mid, mid - 1), "B")

    def get_cell(self, row: int, column: int) -> None or Checker:
        """
        Retrieves the contents of a specific cell on the board.

        Args:
            row (int): The row index of the cell.
            column (int): The column index of the cell.

        Returns:
            None or Checker: The contents of the cell, which is either None (empty)
            or a `Checker` object representing a piece.
        """
        return self.grid[row][column]

    def set_cell(self, row: int, column: int, color: str):
        """
        Places a piece of the specified color at the given position on the board.

        Args:
            row (int): The row index where the piece will be placed.
            column (int): The column index where the piece will be placed.
            color (str): The color of the piece ('W' for white, 'B' for black).
        """
        self.grid[row][column] = Checker((row, column), color)

    def is_full(self) -> bool:
        """
        Checks whether the board is completely filled with pieces.

        Returns:
            bool: True if all cells on the board are occupied, False otherwise.
        """
        return all(cell != None for row in self.grid for cell in row)

    def reset(self):
        """
        Resets the board to its initial state, clearing all pieces and reinitializing the starting configuration.
        """
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.initialize()