"""
This module defines the `Player` class, which represents a player in the Reversi game.

The `Player` class stores player-specific attributes like name, color, and AI status.
It provides methods for making moves and switching between players.
"""

from typing import Tuple

from Board import Board
from MCTSEngine import MCTSEngine
from MiniMax import MiniMaxEngine


class Player:
    """
    Represents a player in the Reversi game.

    Attributes:
        color (str): The color assigned to the player ('W' for white, 'B' for black).
        name (str): The name of the player.
        is_ai (bool): Indicates whether the player is controlled by AI (default is False).

    Methods:
        make_move(): Prompts the player to enter their move and returns it as a tuple of integers.
        switch_player(players): Switches the current player to the other player in a two-player game.
    """

    def __init__(self, color: str, name: str, is_ai: bool = False):
        """
        Initializes a player with a color, name, and AI status.

        Args:
            color (str): The color assigned to the player ('W' or 'B').
            name (str): The name of the player.
            is_ai (bool): Indicates whether the player is an AI. Defaults to False.
        """
        self.color = color
        self.name = name
        self.is_ai = is_ai
        if is_ai:
            from ConsoleDisplay import ConsoleDisplay
            engine_choice = ConsoleDisplay.ask_ai_engine()
            if engine_choice == '1':
                self.ai_engine = MiniMaxEngine(max_depth=4)
            else:
                self.ai_engine = MCTSEngine(simulation_time=200)

    def make_move(self, board: Board) -> Tuple[int, int]:
        """
        Obtains a move in the format "row,col" either through chosen AI engine or human input.

        Returns:
            Tuple[int, int]: The row and column indices of the player's move.

        Actions:
            - Checks if the player is an AI engine and if so acts accordingly.
                - In case it is an AI engine it gets the
                - Otherwise it continuously prompts the player until a valid input is provided.
            - Parses the input into integers and returns them as a tuple.

        Raises:
            ValueError: If the input cannot be parsed into two integers.
        """
        if self.is_ai:
            move = self.ai_engine.get_move(board, self.color)
            if move is None:
                return (-1, -1)
            return move
        else:
            while True:
                try:
                    move = input(f"{self.name} ({self.color}), enter your move as row,col: ")
                    row, col = map(int, move.split(","))
                    return row, col
                except ValueError:
                    print("Invalid input. Please enter your move in the format row,col (e.g., 3,4).")


    def switch_player(self, players: Tuple['Player', 'Player']) -> 'Player':
        """
        Switches the current player to the other player in a two-player game.

        Args:
            players (Tuple[Player, Player]): A tuple containing the two players in the game.

        Returns:
            Player: The other player in the tuple.

        Logic:
            - If the current player matches the first player in the tuple, return the second player.
            - Otherwise, return the first player.
        """
        return players[1] if self == players[0] else players[0]