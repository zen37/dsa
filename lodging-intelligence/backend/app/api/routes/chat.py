from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.llm.openai_client import MissingOpenAIAPIKey
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    document_id: str
    question: str


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        return ChatService().answer(document_id=request.document_id, question=request.question)
    except MissingOpenAIAPIKey as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
