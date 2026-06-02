from __future__ import annotations

from typing import Any

from app.domain.repositories import ChunkRepository
from app.infrastructure.postgres.repositories import PostgresChunkRepository


class BasicRetrievalService:
    def __init__(self, chunk_repo: ChunkRepository | None = None) -> None:
        self.chunk_repo = chunk_repo or PostgresChunkRepository()

    def retrieve(self, *, document_id: str, question: str, limit: int = 5) -> list[dict[str, Any]]:
        return self.chunk_repo.search(document_id, question, limit=limit)
