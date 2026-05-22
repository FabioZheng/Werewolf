from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlayerState:
    player_id: str
    role: str
    model_id: str
    alive: bool = True
    death_phase: str | None = None
    death_reason: str | None = None
    seer_results: dict[str, str] = field(default_factory=dict)
    doctor_history: list[str] = field(default_factory=list)


@dataclass
class GameState:
    game_id: str
    phase: str = "setup"
    day_number: int = 0
    night_number: int = 0
    players: dict[str, PlayerState] = field(default_factory=dict)
    public_messages: list[dict] = field(default_factory=list)
    public_votes: list[dict] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)

    def alive_players(self) -> list[str]:
        return [pid for pid, p in self.players.items() if p.alive]
