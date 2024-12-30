from Checker import Checker


class Board:
    def __init__(self, size: int = 8):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.initialize()

    def initialize(self):
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = Checker((mid - 1, mid - 1), "W")
        self.grid[mid][mid] = Checker((mid, mid), "W")
        self.grid[mid - 1][mid] = Checker((mid - 1, mid), "B")
        self.grid[mid][mid - 1] = Checker((mid, mid - 1), "B")

    def get_cell(self, row: int, column: int) -> Checker:
        return self.grid[row][column]

    def set_cell(self, row: int, column: int, color: str):
        self.grid[row][column] = Checker((row, column), color)

    def is_full(self) -> bool:
        return all(cell != None for row in self.grid for cell in row)

    def reset(self):
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.initialize()