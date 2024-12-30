from typing import Tuple

from win32comext.mapi.mapiutil import prTable


class Player:
    def __init__(self, color: str, name: str, is_ai: bool = False):
        self.color = color
        self.name = name
        self.is_ai = is_ai

    def make_move(self) -> Tuple[int, int]:
        while True:
            try:
                move = input(f"{self.name} ({self.color}), enter your move as row,col: ")
                row, col = map(int, move.split(","))
                return row, col
            except ValueError:
                print("Invalid input. Please enter your move in the format row,col (e.g., 3,4).")

    def switch_player(self, players: Tuple['Player', 'Player']) -> 'Player':
        return players[1] if self == players[0] else players[0]