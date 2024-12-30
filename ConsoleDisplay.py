import os
import platform

from Board import Board
from Player import Player


class ConsoleDisplay:
    @staticmethod
    def start_player_setup():
        print("Player setup:")

    @staticmethod
    def ask_is_ai(default_name: str, color: str) -> bool:
        response = input(f"Is {default_name} ({color}) an AI? (yes/no): ").strip().lower()
        return response == "yes"

    @staticmethod
    def ask_player_name(default_name: str, color: str, is_ai: bool) -> str:
        if is_ai:
            if color == "W":
                return f"AI Biały"
            else:
                return f"AI Czarny"
        return input(f"Enter name for {default_name} ({color}): ").strip()

    @staticmethod
    def clear_console():
        os.system('cls')

    @staticmethod
    def display_board(board: Board, legal_moves: list):
        # ConsoleDisplay.clear_console()
        size = board.size
        # first version of board display
        # print(r"r\c" + "  ".join(f" {column}" for column in range(size)))
        ## second version of board display
        print(r"r\c|" + "".join(f" {column} |" for column in range(size)))
        print(f"---+---+---+---+---+---+---+---+---+")

        for row in range(size):
            # row_string = f" {row}"
            row_string = f" {row} |"
            for column in range(size):
                if (row, column) in legal_moves:
                    # row_string += " (*)"
                    row_string += " * |"
                else:
                    cell = board.get_cell(row, column)
                    # row_string += f" [{' ' if cell is None else cell.get_color()}]"
                    row_string += f" {' ' if cell is None else cell.get_color()} |"
            print(row_string)
            print(f"---+---+---+---+---+---+---+---+---+")

    @staticmethod
    def show_scores(scores: dict[int, int]):
        print(f"Scores: White (W): {scores['W']}, Black (B): {scores['B']}")
        print()

    @staticmethod
    def no_legal_moves_skip_turn(player: Player):
        print(f"{player.name} ({player.color}) has no valid moves. Skipping turn.")

    @staticmethod
    def invalid_move(legal_moves: list):
        print("Invalid move. Please select a valid move from: ", legal_moves)

    @staticmethod
    def game_over(scores: dict[int, int]):
        print("Game Over!")
        print(f"")
        ConsoleDisplay.show_scores(scores)