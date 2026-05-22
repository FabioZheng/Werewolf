from __future__ import annotations
import json
from datetime import datetime


class GameLogger:
    def __init__(self, conn):
        self.conn = conn

    def event(self, game_id: str, event_type: str, phase: str, payload: dict):
        self.conn.execute(
            "INSERT INTO events VALUES (?,?,?,?,?)",
            (game_id, event_type, phase, json.dumps(payload), datetime.utcnow().isoformat()),
        )
        self.conn.commit()
