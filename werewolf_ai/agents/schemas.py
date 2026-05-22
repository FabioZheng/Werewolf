from __future__ import annotations

from typing import Dict, Optional
from pydantic import BaseModel, Field


class DayDiscussionDecision(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    suspicion_scores: Dict[str, float] = Field(default_factory=dict)
    intended_vote: Optional[str] = None
    reasoning_summary: str = Field(min_length=1, max_length=280)


class VoteDecision(BaseModel):
    vote: str
    reasoning_summary: str = Field(min_length=1, max_length=280)


class NightActionDecision(BaseModel):
    action_type: str
    target: str
    reasoning_summary: str = Field(min_length=1, max_length=280)
