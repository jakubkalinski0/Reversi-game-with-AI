from typing import List, Tuple, Dict, Optional
import copy

from AIEngine import AIEngine
from Board import Board
from GameLogic import GameLogic
from MoveLogic import MoveLogic


class MiniMaxEngine(AIEngine):
    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.weights = [
            [100, -20, 10,  5,  5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10,   -2,  1,  1,  1,  1,  -2,  10],
            [5,    -2,  1,  1,  1,  1,  -2,   5],
            [5,    -2,  1,  1,  1,  1,  -2,   5],
            [10,   -2,  1,  1,  1,  1,  -2,  10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10,  5,  5, 10, -20, 100]
        ]
        """
        Reasoning behind the selected weighting distribution:
        
            * Corners (value 100):

                - They have the highest value (100) because they are the strategically most important squares
                - A pawn in a corner cannot be captured
                - A corner can be used to build a stable line of pawns
                - Control of corners often determines the outcome of the game

            * Cells adjacent to corners (value -20 and -50):

                - They have negative values because their capture often allows the opponent to capture a corner
                - Squares diagonally from a corner (-50) are particularly dangerous because they almost always lead to the loss of a corner
                - Squares directly adjacent (-20) are also risky, but less so than squares on the diagonal

            * Edges (values 10, 5):

                - They have moderately positive values
                - Pawns on the edges are more difficult to capture (they can only be attacked from two sides)
                - The value decreases towards the center (10 -> 5), because the outermost squares of the edge are strategically more important

            * Center (values 1):

                - Has low but positive values
                - Control of the center is important for mobility
                - Low values reflect the fact that pawns in the center are easy to capture

            * "Fore-corner" squares (value -2):

                - Slightly negative value
                - Represent squares that can be used to build strategy, but are potentially risky

        This weighting encourages the AI to:

            * Prioritize taking corners
            * Avoid cells adjacent to corners
            * Prefer edges over the center
            * Approach cells preceding corners cautiously
            * Build a stable position from corners and edges
        """

    def get_move(self, board: Board, player_color: str) -> Optional[Tuple[int, int]]:
        _, best_move = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True, player_color)
        return best_move

    # Heuristic
    def evaluate_board(self, board: Board, player_color: str) -> int:
        opponent_color = 'W' if player_color == 'B' else 'B'
        score = 0

        # 1. Positional board evaluation
        position_score = 0
        for r in range(8):
            for c in range(8):
                cell = board.get_cell(r, c)
                if cell:
                    if cell.get_color() == player_color:
                        position_score += self.weights[r][c]
                    elif cell.get_color() == opponent_color:
                        position_score -= self.weights[r][c]

        # 2. Number of pieces
        player_pieces = sum(1 for r in range(8) for c in range(8)
                          if board.get_cell(r, c) and board.get_cell(r, c).get_color() == player_color)
        opponent_pieces = sum(1 for r in range(8) for c in range(8)
                            if board.get_cell(r, c) and board.get_cell(r, c).get_color() == opponent_color)
        piece_difference = player_pieces - opponent_pieces

        # 3. Mobility (number of possible moves)
        player_moves = len(MoveLogic.get_legal_moves(board, player_color))
        opponent_moves = len(MoveLogic.get_legal_moves(board, opponent_color))
        mobility = player_moves - opponent_moves

        # 4. Stability of corners
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        player_corners = sum(1 for r, c in corners
                           if board.get_cell(r, c) and board.get_cell(r, c).get_color() == player_color)
        opponent_corners = sum(1 for r, c in corners
                             if board.get_cell(r, c) and board.get_cell(r, c).get_color() == opponent_color)
        corner_stability = player_corners - opponent_corners

        # Weighted sum of all components
        score = (
            position_score * 1 +
            piece_difference * 10 +
            mobility * 15 +
            corner_stability * 50
        )

        return int(score)

    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizing_player: bool,
                player_color: str) -> Tuple[int, Optional[Tuple[int, int]]]:
        if depth == 0:
            return self.evaluate_board(board, player_color), None

        current_color = player_color if maximizing_player else ('W' if player_color == 'B' else 'B')
        legal_moves = MoveLogic.get_legal_moves(board, current_color)

        if not legal_moves:
            if not MoveLogic.get_legal_moves(board, 'W' if current_color == 'B' else 'B'):
                # Game is over
                final_score = self.evaluate_board(board, player_color)
                return final_score, None
            # Current player must pass
            score, _ = self.minimax(board, depth - 1, alpha, beta, not maximizing_player, player_color)
            return score, None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                GameLogic.apply_move(new_board, move[0], move[1], current_color)

                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False, player_color)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                GameLogic.apply_move(new_board, move[0], move[1], current_color)

                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True, player_color)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move