"""
This module defines the `ConsoleDisplay` class, which provides a console-based user interface for the Reversi game.

The `ConsoleDisplay` class contains static methods for displaying the game board, handling player setup, 
showing scores, and providing feedback to the players during gameplay.
"""

import os
from colorama import Fore, Style, init
from Board import Board
from Player import Player

# Initialize colorama for Windows
init(autoreset=True)

class ConsoleDisplay:
    """
    Provides a console-based user interface for the Reversi game.

    Methods:
        start_player_setup():                                   Displays a prompt for player setup.
        ask_is_ai(default_name, color): Asks if a player is an AI.
        ask_player_name(default_name, color, is_ai): Gets the player's name or assigns a default AI name.
        clear_console(): Clears the console screen.
        display_board(board, legal_moves): Displays the game board, including legal moves.
        show_scores(scores): Displays the current scores of both players.
        no_legal_moves_skip_turn(player): Notifies the player that their turn is skipped due to no valid moves.
        invalid_move(legal_moves): Displays an error message for invalid moves.
        game_over(scores): Displays the final game scores and declares the game over.
    """

    @staticmethod
    def start_player_setup():
        """
        Displays a message to indicate the start of player setup.
        """
        print("Player setup:")

    @staticmethod
    def ask_is_ai(default_name: str, color: str) -> bool:
        """
        Asks the user whether the specified player is an AI.

        Args:
            default_name (str): The default name for the player.
            color (str): The color associated with the player ('W' or 'B').

        Returns:
            bool: True if the player is an AI, False otherwise.
        """
        response = input(f"Is {default_name} ({color}) an AI? (yes/no): ").strip().lower()
        return response == "yes"

    @staticmethod
    def ask_ai_engine() -> str:
        while True:
            engine = input("Choose AI engine (1 for MiniMax, 2 for Monte Carlo): ").strip()
            if engine in ['1', '2']:
                return engine
            print("Invalid choice. Please enter 1 for MiniMax or 2 for Monte Carlo.")

    @staticmethod
    def ask_player_name(default_name: str, color: str, is_ai: bool) -> str:
        """
        Asks the user to enter the player's name or assigns a default name for AI.

        Args:
            default_name (str): The default name for the player.
            color (str): The color associated with the player ('W' or 'B').
            is_ai (bool): Whether the player is an AI.

        Returns:
            str: The name of the player.
        """
        if is_ai:
            return f"AI Biały" if color == "W" else f"AI Czarny"
        return input(f"Enter name for {default_name} ({color}): ").strip()

    @staticmethod
    def clear_console():
        """
        Clears the console screen.
        Works on Windows systems with 'cls'.
        """
        os.system('cls')

    @staticmethod
    def display_board(board: Board, legal_moves: list):
        """
        Displays the current state of the game board, highlighting legal moves.

        Args:
            board (Board): The game board object.
            legal_moves (list): A list of tuples representing the coordinates of legal moves.
        """
        size = board.size
        print(r"r\c|" + "".join(f" {column} |" for column in range(size)))
        print(f"---+---+---+---+---+---+---+---+---+")

        for row in range(size):
            row_string = f" {row} |"
            for column in range(size):
                if (row, column) in legal_moves:
                    row_string += " * |"
                else:
                    cell = board.get_cell(row, column)
                    if cell is None:
                        row_string += "   |"
                    else:
                        color = cell.get_color()
                        if color == "B":
                            row_string += f"{Fore.BLUE} B {Style.RESET_ALL}|"
                        elif color == "W":
                            row_string += f"{Fore.RED} W {Style.RESET_ALL}|"
            print(row_string)
            print(f"---+---+---+---+---+---+---+---+---+")

    @staticmethod
    def show_scores(scores: dict[str, int]):
        """
        Displays the current scores of both players.

        Args:
            scores (dict[str, int]): A dictionary with keys 'W' and 'B' representing player scores.
        """
        print(f"Scores: White (W): {scores['W']}, Black (B): {scores['B']} \n")

    @staticmethod
    def no_legal_moves_skip_turn(player: Player):
        """
        Notifies the player that their turn is skipped due to no legal moves.

        Args:
            player (Player): The player whose turn is being skipped.
        """
        print(f"{player.name} ({player.color}) has no valid moves. Skipping turn.")

    @staticmethod
    def invalid_move(legal_moves: list):
        """
        Displays an error message when the player attempts an invalid move.

        Args:
            legal_moves (list): A list of tuples representing valid move coordinates.
        """
        print("Invalid move. Please select a valid move from: ", legal_moves)

    @staticmethod
    def game_over(scores: dict[str, int]):
        """
        Displays the game-over message and final scores.

        Args:
            scores (dict[str, int]): A dictionary with keys 'W' and 'B' representing final player scores.
        """
        print("Game Over!\n")
        ConsoleDisplay.show_scores(scores)