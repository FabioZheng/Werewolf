from __future__ import annotations

import json
import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenRouterClient:
    def __init__(self, referer: str | None = None, title: str | None = None):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENROUTER_API_KEY")

        resolved_referer = referer or os.environ.get("OPENROUTER_HTTP_REFERER")
        resolved_title = title or os.environ.get("OPENROUTER_X_TITLE")

        headers = {}
        if resolved_referer:
            headers["HTTP-Referer"] = resolved_referer
        if resolved_title:
            headers["X-Title"] = resolved_title

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers=headers or None,
        )

    def complete_json(
        self,
        model_id: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        timeout: float = 60.0,
    ) -> tuple[dict[str, Any], int]:
        start = time.time()
        response = self.client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            timeout=timeout,
        )
        content = response.choices[0].message.content or "{}"
        latency_ms = int((time.time() - start) * 1000)
        return json.loads(content), latency_ms
