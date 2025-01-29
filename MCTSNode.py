import math
from typing import Optional, Tuple

from Board import Board
from MoveLogic import MoveLogic


class MCTSNode:
    def __init__(self, board: Board, player_color: str, move: Optional[Tuple[int, int]] = None, parent=None):
        self.board = board
        self.player_color = player_color
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = MoveLogic.get_legal_moves(board, player_color)

    def uct_value(self, exploration_constant: float) -> float:
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)