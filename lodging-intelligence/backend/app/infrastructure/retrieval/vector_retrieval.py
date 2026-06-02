from __future__ import annotations


class VectorRetrievalService:
    """Placeholder boundary for pgvector-backed retrieval.

    The initial migration omits the embedding column because pgvector availability
    is local-environment dependent. This class is intentionally small so vector
    search can be added later without changing API routes.
    """

    def retrieve(self, *, document_id: str, question: str, limit: int = 5) -> list[dict]:
        raise NotImplementedError("Vector retrieval is not enabled for the MVP.")
