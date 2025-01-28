"""
This module defines the `Checker` class, which represents individual game pieces in Reversi.

The `Checker` class encapsulates the position and color of a piece on the board, allowing for color flipping and retrieval.
"""

from typing import Tuple

class Checker:
    """
    Represents a single game piece (checker) in Reversi.

    Attributes:
        position (Tuple[int, int]): The (row, column) position of the checker on the board.
        color (str): The color of the checker ('W' for white, 'B' for black).

    Methods:
        flip(): Flips the color of the checker.
        get_color(): Returns the current color of the checker.
    """
    def __init__(self, position: Tuple[int, int], color: str):
        """
        Initializes a new checker with a specified position and color.

        Args:
            position (Tuple[int, int]): The (row, column) position of the checker.
            color (str): The color of the checker ('W' for white, 'B' for black).
        """
        self.position = position
        self.color = color

    def flip(self):
        """
        Flips the color of the checker.

        Changes the color from black ('B') to white ('W'), or vice versa.
        """
        self.color = "W" if self.color == "B" else "B"

    def get_color(self) -> str:
        """
        Returns the current color of the checker.

        Returns:
            str: The color of the checker ('W' or 'B').
        """
        return self.color