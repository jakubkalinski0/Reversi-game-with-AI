from Board import Board
from MoveLogic import MoveLogic
from Player import Player


class GameState:
    def __init__(self, board: Board, player: Player):
        self.board = board
        self.current_player = player
        self.scores = {"W": 0, "B": 0}
        self.legal_moves = []
        self.update_scores()
        self.update_legal_moves()

    def update_scores(self):
        self.scores = {
            "W": sum(1 for row in self.board.grid for cell in row if cell and cell.get_color() == "W"),
            "B": sum(1 for row in self.board.grid for cell in row if cell and cell.get_color() == "B"),
        }

    def update_legal_moves(self):
        self.legal_moves = MoveLogic.get_legal_moves(self.board, self.current_player.color)

    def is_game_over(self) -> bool:
        return self.board.is_full() or not self.legal_moves