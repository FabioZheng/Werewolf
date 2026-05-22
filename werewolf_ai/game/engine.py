from __future__ import annotations

import json
import random
import uuid
from datetime import datetime

from game.state import GameState, PlayerState
from game.win_conditions import check_win


class WerewolfEngine:
    def __init__(self, agents: dict, role_map: dict[str, str], logger, conn, seed: int = 42, discussion_rounds: int = 1):
        self.random = random.Random(seed)
        self.agents = agents
        self.logger = logger
        self.conn = conn
        self.state = GameState(game_id=str(uuid.uuid4()))
        self.discussion_rounds = discussion_rounds
        for pid, agent in agents.items():
            self.state.players[pid] = PlayerState(player_id=pid, role=role_map[pid], model_id=agent.model_id)

    def run(self, config: dict) -> str:
        self._insert_game(config)
        winner = None
        while not winner:
            self._night_phase()
            winner = self._check_win()
            if winner:
                break
            self._day_phase()
            winner = self._check_win()
        self.conn.execute("UPDATE games SET finished_at=?, winning_team=? WHERE game_id=?", (datetime.utcnow().isoformat(), winner, self.state.game_id))
        self.conn.commit()
        return winner

    def _public_state(self):
        return {"alive_players": self.state.alive_players(), "day_number": self.state.day_number, "phase": self.state.phase}

    def _night_phase(self):
        self.state.phase = "night"
        self.state.night_number += 1
        kills, protect = [], None
        alive = self.state.alive_players()
        for pid in alive:
            p = self.state.players[pid]
            if p.role == "werewolf":
                d = self.agents[pid].decide(self._public_state(), {"role": p.role}, "night_action")
                kills.append(d.get("target"))
            elif p.role == "doctor":
                d = self.agents[pid].decide(self._public_state(), {"role": p.role}, "night_action")
                protect = d.get("target")
            elif p.role == "seer":
                d = self.agents[pid].decide(self._public_state(), {"role": p.role}, "night_action")
                tgt = d.get("target")
                if tgt in self.state.players:
                    p.seer_results[tgt] = self.state.players[tgt].role
        if kills:
            target = sorted(kills)[0]
            if target != protect and target in alive:
                self._kill(target, "night", "werewolf_attack")

    def _day_phase(self):
        self.state.phase = "day_discussion"
        self.state.day_number += 1
        for r in range(self.discussion_rounds):
            for pid in self.state.alive_players():
                p = self.state.players[pid]
                d = self.agents[pid].decide(self._public_state(), {"role": p.role}, "discussion")
                self.conn.execute("INSERT INTO messages VALUES (?,?,?,?,?,?,?,?,?,?,?)", (self.state.game_id, self.state.phase, self.state.day_number, r + 1, pid, p.model_id, d.get("message"), d.get("reasoning_summary"), json.dumps(d), 1, d.get("latency_ms", 0)))
        self.state.phase = "voting"
        votes = {}
        alive = self.state.alive_players()
        for pid in alive:
            p = self.state.players[pid]
            d = self.agents[pid].decide(self._public_state(), {"role": p.role}, "vote")
            target = d.get("vote") if d.get("vote") in alive else sorted([x for x in alive if x != pid])[0]
            votes[pid] = target
            self.conn.execute("INSERT INTO votes VALUES (?,?,?,?,?)", (self.state.game_id, self.state.day_number, pid, target, d.get("reasoning_summary")))
        self.conn.commit()
        self.state.phase = "elimination"
        tally = {}
        for t in votes.values():
            tally[t] = tally.get(t, 0) + 1
        elim = sorted(tally.items(), key=lambda x: (-x[1], x[0]))[0][0]
        self._kill(elim, "day", "voted_out")

    def _kill(self, player_id: str, phase: str, reason: str):
        p = self.state.players[player_id]
        p.alive = False
        p.death_phase = phase
        p.death_reason = reason

    def _check_win(self):
        roles = [self.state.players[p].role for p in self.state.alive_players()]
        return check_win(roles)

    def _insert_game(self, config: dict):
        self.conn.execute("INSERT INTO games VALUES (?,?,?,?,?,?)", (self.state.game_id, datetime.utcnow().isoformat(), None, None, json.dumps(config), config.get("seed", 42)))
        for pid, p in self.state.players.items():
            self.conn.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?)", (self.state.game_id, pid, p.role, p.model_id, 1, None, None))
        self.conn.commit()
