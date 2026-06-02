from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import UploadFile

from app.domain.models import SUPPORTED_FILE_TYPES
from app.domain.repositories import (
    ChunkRepository,
    DocumentRepository,
    ExtractedTableRepository,
    ExtractionRepository,
)
from app.infrastructure.parsers.parser_factory import get_parser
from app.infrastructure.postgres.repositories import (
    PostgresChunkRepository,
    PostgresDocumentRepository,
    PostgresExtractedTableRepository,
    PostgresExtractionRepository,
)
from app.infrastructure.storage.local_storage import LocalStorageService, detect_file_type
from app.services.chunking import build_chunks
from app.services.classification_service import ClassificationService
from app.services.extraction_service import ExtractionService
from app.services.hotel_service import HotelService
from app.services.operating_statement_service import OperatingStatementService


SUPPORTED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
    "application/csv",
}


class UnsupportedFileType(ValueError):
    pass


class DocumentProcessingService:
    def __init__(
        self,
        *,
        document_repo: DocumentRepository | None = None,
        chunk_repo: ChunkRepository | None = None,
        table_repo: ExtractedTableRepository | None = None,
        extraction_repo: ExtractionRepository | None = None,
        storage: LocalStorageService | None = None,
        classification_service: ClassificationService | None = None,
        extraction_service: ExtractionService | None = None,
        hotel_service: HotelService | None = None,
        operating_statement_service: OperatingStatementService | None = None,
    ) -> None:
        self.document_repo = document_repo or PostgresDocumentRepository()
        self.chunk_repo = chunk_repo or PostgresChunkRepository()
        self.table_repo = table_repo or PostgresExtractedTableRepository()
        self.extraction_repo = extraction_repo or PostgresExtractionRepository()
        self.storage = storage or LocalStorageService()
        self.classification_service = classification_service or ClassificationService()
        self.extraction_service = extraction_service or ExtractionService()
        self.hotel_service = hotel_service or HotelService(document_repo=self.document_repo)
        self.operating_statement_service = (
            operating_statement_service or OperatingStatementService()
        )

    async def upload(self, *, upload_file: UploadFile, hotel_id: str | None = None) -> dict[str, Any]:
        file_type = detect_file_type(upload_file.filename or "")
        if file_type not in SUPPORTED_FILE_TYPES:
            raise UnsupportedFileType("Supported file types are PDF, DOCX, XLSX, and CSV.")

        if upload_file.content_type and upload_file.content_type not in SUPPORTED_MIME_TYPES:
            if upload_file.content_type != "application/octet-stream":
                raise UnsupportedFileType("Unsupported MIME type for lodging document upload.")

        filename, storage_path = await self.storage.save_upload(upload_file)
        return self.document_repo.create(
            hotel_id=hotel_id,
            filename=filename,
            original_filename=upload_file.filename or filename,
            file_type=file_type,
            mime_type=upload_file.content_type,
            storage_path=storage_path,
        )

    def process_document(self, document_id: str) -> None:
        document = self.document_repo.get(document_id)
        if not document:
            return

        try:
            self.document_repo.update_status(document_id, "processing")
            parser = get_parser(document["file_type"])
            parsed = parser.parse(Path(document["storage_path"]))
            self.document_repo.update_parser(document_id, parser.__class__.__name__)

            self.table_repo.add_many(
                document_id,
                [
                    {
                        "source_name": table.source_name,
                        "page_number": table.page_number,
                        "sheet_name": table.sheet_name,
                        "table_index": index,
                        "raw_json": {"rows": table.rows},
                    }
                    for index, table in enumerate(parsed.tables)
                ],
            )

            chunks = self.chunk_repo.add_many(document_id, build_chunks(parsed))
            context = self._context_from_chunks(chunks)

            classification = self.classification_service.classify(context)
            self.document_repo.update_classification(
                document_id, classification.document_type, classification.confidence
            )

            summary = self.extraction_service.extract_summary(context).model_dump()
            self.extraction_repo.create(
                document_id=document_id,
                extraction_type="document_summary",
                raw_json=summary,
                confidence=summary.get("confidence"),
            )

            profile = self.extraction_service.extract_property_profile(context).model_dump()
            self.extraction_repo.create(
                document_id=document_id,
                extraction_type="property_profile",
                raw_json=profile,
                confidence=profile.get("confidence"),
            )
            hotel = self.hotel_service.normalize_property_profile(
                document_id=document_id, hotel_id=document.get("hotel_id"), profile=profile
            )
            effective_hotel_id = document.get("hotel_id") or (hotel or {}).get("id")

            operating = self.extraction_service.extract_operating_statement(context).model_dump()
            self.extraction_repo.create(
                document_id=document_id,
                extraction_type="operating_statement",
                raw_json=operating,
                confidence=operating.get("confidence"),
            )
            self.operating_statement_service.normalize(
                hotel_id=effective_hotel_id, document_id=document_id, extraction=operating
            )

            self.document_repo.update_status(document_id, "processed")
        except Exception as exc:
            self.document_repo.update_status(document_id, "failed", str(exc))

    @staticmethod
    def _context_from_chunks(chunks: list[dict[str, Any]], limit: int = 16000) -> str:
        context_parts = []
        total = 0
        for chunk in chunks:
            citation = []
            if chunk.get("page_number") is not None:
                citation.append(f"page {chunk['page_number']}")
            if chunk.get("sheet_name"):
                citation.append(f"sheet {chunk['sheet_name']}")
            if chunk.get("section_name"):
                citation.append(f"section {chunk['section_name']}")
            prefix = f"[{', '.join(citation)}] " if citation else ""
            text = prefix + chunk.get("chunk_text", "")
            if total + len(text) > limit:
                break
            context_parts.append(text)
            total += len(text)
        return "\n\n".join(context_parts)
