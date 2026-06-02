from __future__ import annotations

from typing import Any

from app.domain.repositories import DocumentRepository
from app.infrastructure.postgres.repositories import PostgresDocumentRepository


class DocumentService:
    def __init__(self, document_repo: DocumentRepository | None = None) -> None:
        self.document_repo = document_repo or PostgresDocumentRepository()

    def list_documents(self) -> list[dict[str, Any]]:
        return self.document_repo.list()

    def get_document(self, document_id: str) -> dict[str, Any] | None:
        return self.document_repo.get(document_id)
