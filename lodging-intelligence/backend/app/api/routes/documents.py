from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile, status

from app.services.document_service import DocumentService
from app.services.document_processing_service import (
    DocumentProcessingService,
    UnsupportedFileType,
)

router = APIRouter(prefix="/api/documents", tags=["documents"])


def get_document_service() -> DocumentProcessingService:
    return DocumentProcessingService()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: Annotated[UploadFile, File()],
    hotel_id: Annotated[str | None, Form()] = None,
):
    service = get_document_service()
    try:
        document = await service.upload(upload_file=file, hotel_id=hotel_id)
    except UnsupportedFileType as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    background_tasks.add_task(service.process_document, document["id"])
    return {
        "document_id": document["id"],
        "hotel_id": document.get("hotel_id"),
        "filename": document["filename"],
        "file_type": document["file_type"],
        "processing_status": document["processing_status"],
    }


@router.get("")
def list_documents():
    return DocumentService().list_documents()


@router.get("/{document_id}")
def get_document(document_id: str):
    document = DocumentService().get_document(document_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
    return document
