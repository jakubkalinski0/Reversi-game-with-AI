"""
This script serves as the entry point for the Reversi game.

It initializes the game by creating an instance of the `Game` class and starts the gameplay loop.
The `Game` class is responsible for managing the overall flow of the game, including player turns, board state, and game logic.
"""

from Game import Game

if __name__ == "__main__":
    """
    Entry point of the Reversi game.

    Actions:
        - Creates an instance of the `Game` class.
        - Calls the `start` method to initiate the game loop.
    """
    game = Game()  # Instantiate the main game class.
    game.start()   # Begin the game loop.