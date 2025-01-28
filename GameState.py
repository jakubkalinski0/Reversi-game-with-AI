"""
This module defines the `GameState` class, which manages the overall state of the Reversi game.

The `GameState` class keeps track of the game board, the current player, scores, and legal moves.
It provides methods to update scores, determine legal moves, and check whether the game is over.
"""
from Board import Board
from MoveLogic import MoveLogic
from Player import Player

class GameState:
    """
    Manages the overall state of the Reversi game, including the board, players, scores, and legal moves.

    Attributes:
        board (Board): The game board instance representing the current state of the game.
        current_player (Player): The player whose turn it is to make a move.
        scores (dict): A dictionary holding the current scores for both colors ('W' for white, 'B' for black).
        legal_moves (list): A list of tuples representing the coordinates of all valid moves for the current player.

    Methods:
        update_scores(): Updates the scores based on the current state of the board.
        update_legal_moves(): Determines and updates the list of legal moves for the current player.
        is_game_over(): Checks whether the game is over by evaluating the board's state and legal moves.
    """

    def __init__(self, board: Board, player: Player):
        """
        Initializes the game state with a board, a current player, and default scores and legal moves.

        Args:
            board (Board): The game board instance representing the current state of the game.
            player (Player): The player whose turn it is to make the next move.

        Actions:
            - Initializes the board and current player.
            - Sets default scores to 0 for both colors.
            - Calculates the initial scores and legal moves based on the board's state.
        """
        self.board = board
        self.current_player = player
        self.scores = {"W": 0, "B": 0}
        self.legal_moves = []
        self.update_scores()
        self.update_legal_moves()

    def update_scores(self):
        """
        Updates the scores for both players by counting the pieces of each color on the board.

        Actions:
            - Iterates through the board's grid.
            - Counts all pieces with color 'W' (white) and 'B' (black).
            - Updates the `scores` dictionary with the counts.
        """
        self.scores = {
            "W": sum(1 for row in self.board.grid for cell in row if cell and cell.get_color() == "W"),
            "B": sum(1 for row in self.board.grid for cell in row if cell and cell.get_color() == "B"),
        }

    def update_legal_moves(self):
        """
        Updates the list of legal moves for the current player by using the `MoveLogic` module.

        Actions:
            - Calls the `get_legal_moves` method from `MoveLogic`.
            - Updates the `legal_moves` attribute with the result.
        """
        self.legal_moves = MoveLogic.get_legal_moves(self.board, self.current_player.color)

    def is_game_over(self) -> bool:
        """
        Checks whether the game is over by evaluating the board's state and legal moves.

        Returns:
            bool: True if the game is over (board is full or no legal moves exist), otherwise False.
        """
        return self.board.is_full() or not self.legal_moves