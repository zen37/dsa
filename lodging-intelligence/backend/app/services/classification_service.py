from __future__ import annotations

from pydantic import BaseModel, Field

from app.domain.models import ALLOWED_DOCUMENT_TYPES
from app.infrastructure.llm.openai_client import OpenAIClient


class ClassificationResult(BaseModel):
    document_type: str = "unknown"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    detected_sections: list[str] = Field(default_factory=list)


class ClassificationService:
    def __init__(self, llm: OpenAIClient | None = None) -> None:
        self.llm = llm or OpenAIClient()

    def classify(self, context: str) -> ClassificationResult:
        system = (
            "You classify lodging and hotel documents. Return only JSON. "
            "Use one allowed document_type value. If evidence is weak, use unknown."
        )
        user = f"""
Allowed document_type values:
{sorted(ALLOWED_DOCUMENT_TYPES)}

Return JSON shaped as:
{{
  "document_type": "offering_memorandum",
  "confidence": 0.94,
  "detected_sections": ["Executive Summary"]
}}

Document excerpt:
{context[:8000]}
"""
        raw = self.llm.json_chat(system=system, user=user)
        result = ClassificationResult.model_validate(raw)
        if result.document_type not in ALLOWED_DOCUMENT_TYPES or result.confidence < 0.5:
            result.document_type = "unknown"
        return result
