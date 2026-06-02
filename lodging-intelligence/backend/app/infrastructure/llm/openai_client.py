from __future__ import annotations

import json
import re
from typing import Any

from app.config import get_settings


class MissingOpenAIAPIKey(RuntimeError):
    pass


def _extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?", "", stripped).strip()
        stripped = re.sub(r"```$", "", stripped).strip()
    return json.loads(stripped)


class OpenAIClient:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key if api_key is not None else settings.openai_api_key
        self.model = model or settings.openai_model

    def _client(self):
        if not self.api_key:
            raise MissingOpenAIAPIKey(
                "OPENAI_API_KEY is not configured. Set it before classification, extraction, or chat."
            )
        from openai import OpenAI

        return OpenAI(api_key=self.api_key)

    def json_chat(self, *, system: str, user: str) -> dict[str, Any]:
        response = self._client().chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        content = response.choices[0].message.content or "{}"
        return _extract_json(content)

    def text_chat(self, *, system: str, user: str) -> str:
        response = self._client().chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""
