import copy
import random
from typing import Optional, Tuple

from AIEngine import AIEngine
from Board import Board
from GameLogic import GameLogic
from MCTSNode import MCTSNode
from MoveLogic import MoveLogic


class MCTSEngine(AIEngine):
    def __init__(self, simulation_time: int = 200, exploration_constant: float = 1.414):
        self.simulation_time = simulation_time  # Number of simulations to run
        self.exploration_constant = exploration_constant

    def get_move(self, board: Board, player_color: str) -> Optional[Tuple[int, int]]:
        root = MCTSNode(board, player_color)

        for _ in range(self.simulation_time):
            node = self.select(root)
            if not node.board.is_full() and node.untried_moves:
                node = self.expand(node)
            simulation_result = self.simulate(node)
            self.backpropagate(node, simulation_result)

        # Choose the move with the most visits
        if not root.children:
            return None

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move

    def select(self, node: MCTSNode) -> MCTSNode:
        while node.untried_moves == [] and node.children != []:
            node = max(node.children, key=lambda c: c.uct_value(self.exploration_constant))
        return node

    def expand(self, node: MCTSNode) -> MCTSNode:
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        new_board = copy.deepcopy(node.board)
        GameLogic.apply_move(new_board, move[0], move[1], node.player_color)

        next_color = 'W' if node.player_color == 'B' else 'B'
        child_node = MCTSNode(
            board=new_board,
            player_color=next_color,
            move=move,
            parent=node
        )
        node.children.append(child_node)
        return child_node

    def simulate(self, node: MCTSNode) -> bool:
        board = copy.deepcopy(node.board)
        current_color = node.player_color
        original_color = node.player_color

        while not board.is_full():
            moves = MoveLogic.get_legal_moves(board, current_color)
            if not moves:
                if not MoveLogic.get_legal_moves(board, 'W' if current_color == 'B' else 'B'):
                    break
                current_color = 'W' if current_color == 'B' else 'B'
                continue

            move = random.choice(moves)
            GameLogic.apply_move(board, move[0], move[1], current_color)
            current_color = 'W' if current_color == 'B' else 'B'

        # Count pieces to determine winner
        white_count = sum(1 for r in range(8) for c in range(8)
                          if board.get_cell(r, c) and board.get_cell(r, c).get_color() == 'W')
        black_count = sum(1 for r in range(8) for c in range(8)
                          if board.get_cell(r, c) and board.get_cell(r, c).get_color() == 'B')

        if original_color == 'B':
            return black_count > white_count
        return white_count > black_count

    def backpropagate(self, node: MCTSNode, result: bool):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent
            if node:  # Flip the result for the parent node
                result = not result