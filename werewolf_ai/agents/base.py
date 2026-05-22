from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePlayerAgent(ABC):
    def __init__(self, player_id: str, model_id: str):
        self.player_id = player_id
        self.model_id = model_id

    @abstractmethod
    def decide(self, game_state: dict[str, Any], private_state: dict[str, Any], task: str) -> dict[str, Any]:
        raise NotImplementedError
