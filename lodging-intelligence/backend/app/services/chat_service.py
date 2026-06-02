from __future__ import annotations

from typing import Any

from app.infrastructure.llm.openai_client import OpenAIClient
from app.infrastructure.retrieval.basic_retrieval import BasicRetrievalService


NOT_ENOUGH_INFORMATION = "The document does not provide enough information to answer that question."


class ChatService:
    def __init__(
        self,
        retrieval_service: BasicRetrievalService | None = None,
        llm: OpenAIClient | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service or BasicRetrievalService()
        self.llm = llm or OpenAIClient()

    def answer(self, *, document_id: str, question: str) -> dict[str, Any]:
        chunks = self.retrieval_service.retrieve(document_id=document_id, question=question, limit=5)
        if not chunks:
            return {"answer": NOT_ENOUGH_INFORMATION, "citations": []}

        context = "\n\n".join(
            f"Chunk {chunk['id']} "
            f"(page={chunk.get('page_number')}, sheet={chunk.get('sheet_name')}, "
            f"section={chunk.get('section_name')}):\n{chunk.get('chunk_text', '')}"
            for chunk in chunks
        )
        answer = self.llm.text_chat(
            system=(
                "You answer questions about lodging documents only from the supplied chunks. "
                "If the answer is missing, say the document does not provide enough information. "
                "Do not invent hotel facts."
            ),
            user=f"Question: {question}\n\nRetrieved chunks:\n{context}",
        ).strip()
        if not answer:
            answer = NOT_ENOUGH_INFORMATION

        return {
            "answer": answer,
            "citations": [
                {
                    "document_id": document_id,
                    "page_number": chunk.get("page_number"),
                    "sheet_name": chunk.get("sheet_name"),
                    "section_name": chunk.get("section_name"),
                    "chunk_id": chunk["id"],
                }
                for chunk in chunks
            ],
        }
