from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Tuple, Union
import uuid
import json
from enum import Enum

from Board import Board
from Checker import Checker
from GameLogic import GameLogic
from MoveLogic import MoveLogic
from Player import Player
from MCTSEngine import MCTSEngine
from MiniMaxEngine import MiniMaxEngine

app = FastAPI(title="Reversi Game API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlayerType(str, Enum):
    HUMAN = "human"
    AI_MINIMAX = "minimax"
    AI_MCTS = "mcts"


class CreateGameRequest(BaseModel):
    player1: PlayerType = PlayerType.HUMAN
    player2: PlayerType = PlayerType.AI_MINIMAX
    player1_name: Optional[str] = "Player 1"
    player2_name: Optional[str] = "Player 2"
    board_size: int = 8


class MoveRequest(BaseModel):
    row: int
    col: int


class GameState(BaseModel):
    board: List[List[Optional[str]]]
    current_player: str
    scores: Dict[str, int]
    legal_moves: List[List[int]]
    game_over: bool
    winner: Optional[str] = None
    message: Optional[str] = None


games = {}


def board_to_array(board: Board) -> List[List[Optional[str]]]:
    return [
        [board.get_cell(row, col).get_color() if board.get_cell(row, col) else None
         for col in range(board.size)]
        for row in range(board.size)
    ]


def get_legal_moves(board: Board, color: str) -> List[List[int]]:
    return [[row, col] for row, col in MoveLogic.get_legal_moves(board, color)]


@app.post("/games", response_model=Dict[str, Union[str, GameState]])
async def create_game(request: CreateGameRequest):
    """Create a new Reversi game"""
    game_id = str(uuid.uuid4())

    board = Board(size=request.board_size)

    players = []

    if request.player1 == PlayerType.HUMAN:
        players.append(Player("B", request.player1_name, is_ai=False))
    elif request.player1 == PlayerType.AI_MINIMAX:
        player = Player("B", request.player1_name, is_ai=True)
        player.ai_engine = MiniMaxEngine(max_depth=4)
        players.append(player)
    else:  # MCTS
        player = Player("B", request.player1_name, is_ai=True)
        player.ai_engine = MCTSEngine(simulation_time=200)
        players.append(player)

    if request.player2 == PlayerType.HUMAN:
        players.append(Player("W", request.player2_name, is_ai=False))
    elif request.player2 == PlayerType.AI_MINIMAX:
        player = Player("W", request.player2_name, is_ai=True)
        player.ai_engine = MiniMaxEngine(max_depth=4)
        players.append(player)
    else:  # MCTS
        player = Player("W", request.player2_name, is_ai=True)
        player.ai_engine = MCTSEngine(simulation_time=200)
        players.append(player)

    # Store game state
    games[game_id] = {
        "board": board,
        "players": players,
        "current_player_index": 0,
        "game_over": False
    }

    legal_moves = get_legal_moves(board, players[0].color)

    scores = {
        "W": sum(1 for row in board.grid for cell in row if cell and cell.get_color() == "W"),
        "B": sum(1 for row in board.grid for cell in row if cell and cell.get_color() == "B")
    }

    # Return initial game state
    return {
        "game_id": game_id,
        "state": GameState(
            board=board_to_array(board),
            current_player=players[0].color,
            scores=scores,
            legal_moves=legal_moves,
            game_over=False
        )
    }


@app.get("/games/{game_id}", response_model=GameState)
async def get_game_state(game_id: str):
    """Get the current state of a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    board = game["board"]
    players = game["players"]
    current_player_idx = game["current_player_index"]
    current_player = players[current_player_idx]

    legal_moves = get_legal_moves(board, current_player.color)

    scores = {
        "W": sum(1 for row in board.grid for cell in row if cell and cell.get_color() == "W"),
        "B": sum(1 for row in board.grid for cell in row if cell and cell.get_color() == "B")
    }

    is_game_over = board.is_full() or (not legal_moves and
                                       not get_legal_moves(board, "W" if current_player.color == "B" else "B"))

    winner = None
    if is_game_over:
        if scores["W"] > scores["B"]:
            winner = "W"
        elif scores["B"] > scores["W"]:
            winner = "B"
        game["game_over"] = True

    message = None
    if not legal_moves and not is_game_over:
        message = f"No legal moves for {current_player.name}. Turn skipped."

    return GameState(
        board=board_to_array(board),
        current_player=current_player.color,
        scores=scores,
        legal_moves=legal_moves,
        game_over=is_game_over,
        winner=winner,
        message=message
    )


@app.post("/games/{game_id}/move", response_model=GameState)
async def make_move(game_id: str, move: MoveRequest):
    """Make a move in the game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    if game["game_over"]:
        raise HTTPException(status_code=400, detail="Game is already over")

    board = game["board"]
    players = game["players"]
    current_player_idx = game["current_player_index"]
    current_player = players[current_player_idx]

    legal_moves = MoveLogic.get_legal_moves(board, current_player.color)

    if current_player.is_ai:
        ai_move = current_player.ai_engine.get_move(board, current_player.color)
        if ai_move:
            move = MoveRequest(row=ai_move[0], col=ai_move[1])
        else:
            next_player_idx = (current_player_idx + 1) % len(players)
            game["current_player_index"] = next_player_idx

            return await get_game_state(game_id)

    if (move.row, move.col) not in legal_moves:
        raise HTTPException(status_code=400, detail="Invalid move")

    GameLogic.apply_move(board, move.row, move.col, current_player.color)

    next_player_idx = (current_player_idx + 1) % len(players)
    game["current_player_index"] = next_player_idx

    return await get_game_state(game_id)


@app.post("/games/{game_id}/ai-move", response_model=GameState)
async def make_ai_move(game_id: str):
    """Let the AI make a move if it's its turn"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]
    current_player = game["players"][game["current_player_index"]]

    if not current_player.is_ai:
        raise HTTPException(status_code=400, detail="Current player is not an AI")

    return await make_move(game_id, MoveRequest(row=0, col=0))  # Dummy values, will be ignored


@app.delete("/games/{game_id}")
async def delete_game(game_id: str):
    """Delete a game"""
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    del games[game_id]
    return {"message": "Game deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)