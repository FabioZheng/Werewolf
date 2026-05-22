from __future__ import annotations

import random
from collections import Counter

from agents.openrouter_agent import OpenRouterPlayerAgent
from game.engine import WerewolfEngine
from storage.db import init_db


def build_role_map(role_counts: dict[str, int], seed: int):
    roles = []
    for role, count in role_counts.items():
        roles.extend([role] * count)
    rng = random.Random(seed)
    rng.shuffle(roles)
    return {f"P{i+1}": role for i, role in enumerate(roles)}


def run_once(db_path: str, role_counts: dict[str, int], model_assignments: dict[str, str], temperature: float, max_tokens: int, seed: int, discussion_rounds: int):
    conn = init_db(db_path)
    role_map = build_role_map(role_counts, seed)
    agents = {
        pid: OpenRouterPlayerAgent(pid, model_assignments[pid], role_map[pid], temperature, max_tokens)
        for pid in role_map
    }
    engine = WerewolfEngine(agents, role_map, logger=None, conn=conn, seed=seed, discussion_rounds=discussion_rounds)
    return engine.run({"seed": seed, "role_counts": role_counts, "model_assignments": model_assignments, "temperature": temperature, "max_tokens": max_tokens})


def rotate_models(players: list[str], models: list[str], game_idx: int) -> dict[str, str]:
    return {p: models[(i + game_idx) % len(models)] for i, p in enumerate(players)}
