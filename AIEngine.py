from abc import ABC, abstractmethod
from typing import Optional, Tuple

from Board import Board


class AIEngine(ABC):
    """Abstract base class for AI engines"""
    @abstractmethod
    def get_move(self, board: Board, player_color: str) -> Optional[Tuple[int, int]]:
        pass