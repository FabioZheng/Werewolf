from __future__ import annotations

import json
from typing import Any

from agents.base import BasePlayerAgent
from agents.openrouter_client import OpenRouterClient
from agents.prompts import system_prompt_for_role
from agents.schemas import DayDiscussionDecision, NightActionDecision, VoteDecision


class OpenRouterPlayerAgent(BasePlayerAgent):
    def __init__(self, player_id: str, model_id: str, role: str, temperature: float, max_tokens: int):
        super().__init__(player_id, model_id)
        self.role = role
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenRouterClient()

    def decide(self, game_state: dict[str, Any], private_state: dict[str, Any], task: str) -> dict[str, Any]:
        prompt = json.dumps({"task": task, "game_state": game_state, "private_state": private_state})
        system = system_prompt_for_role(self.role)
        for _ in range(2):
            try:
                payload, latency = self.client.complete_json(self.model_id, system, prompt, self.temperature, self.max_tokens)
                payload["latency_ms"] = latency
                return self._validate(task, payload)
            except Exception:
                continue
        return self._fallback(task, game_state)

    def _validate(self, task: str, payload: dict[str, Any]) -> dict[str, Any]:
        if task == "discussion":
            return DayDiscussionDecision.model_validate(payload).model_dump()
        if task == "vote":
            return VoteDecision.model_validate(payload).model_dump()
        return NightActionDecision.model_validate(payload).model_dump()

    def _fallback(self, task: str, game_state: dict[str, Any]) -> dict[str, Any]:
        alive = sorted(game_state.get("alive_players", []))
        target = alive[0] if alive else self.player_id
        if task == "discussion":
            return {"message": "I am uncertain; sharing minimal thoughts.", "suspicion_scores": {}, "intended_vote": target, "reasoning_summary": "Fallback due to invalid model output."}
        if task == "vote":
            return {"vote": target, "reasoning_summary": "Fallback due to invalid model output."}
        return {"action_type": "fallback_action", "target": target, "reasoning_summary": "Fallback due to invalid model output."}
