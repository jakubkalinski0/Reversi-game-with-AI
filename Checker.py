from typing import Tuple

class Checker:
    def __init__(self, position: Tuple[int, int], color: str):
        self.position = position
        self.color = color

    def flip(self):
        self.color = "W" if self.color == "B" else "B"

    def get_color(self) -> str:
        return self.color