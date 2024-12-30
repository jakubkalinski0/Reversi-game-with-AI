from typing import Tuple

from Board import Board
from ConsoleDisplay import ConsoleDisplay
from GameLogic import GameLogic
from GameState import GameState
from Player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.display = ConsoleDisplay()
        self.players = self.setup_players()
        self.state = GameState(self.board, self.players[0])

    def setup_players(self) -> Tuple[Player, Player]:
        players: list[Player] = []  # Explicitly type the list
        for color, default_name in [("B", "Player 1"), ("W", "Player 2")]:
            is_ai = self.display.ask_is_ai(default_name, color)
            name = self.display.ask_player_name(default_name, color, is_ai)
            players.append(Player(color=color, name=name, is_ai=is_ai))
        return tuple(players)

    def start(self):
        while not self.state.is_game_over():
            self.play_turn()
            self.state.current_player = self.state.current_player.switch_player(self.players)
        self.end_game()

    def play_turn(self):
        self.state.update_legal_moves()
        self.state.update_scores()
        self.display.display_board(self.board, self.state.legal_moves)
        self.display.show_scores(self.state.scores)

        if not self.state.legal_moves:
            self.display.no_legal_moves_skip_turn(self.state.current_player)
            return

        while True:
            row, col = self.state.current_player.make_move()
            if (row, col) in self.state.legal_moves:
                break
            self.display.invalid_move(self.state.legal_moves)

        GameLogic.apply_move(self.board, row, col, self.state.current_player.color)

    def end_game(self):
        self.display.display_board(self.board, self.state.legal_moves)
        self.state.update_scores()
        self.display.show_scores(self.state.scores)
        self.display.game_over(self.state.scores)