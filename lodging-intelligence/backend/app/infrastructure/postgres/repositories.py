from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from decimal import Decimal
from typing import Any
import re
import uuid

from sqlalchemy import func, select

from app.infrastructure.postgres.models import (
    Document,
    DocumentChunk,
    ExtractedTable,
    Extraction,
    Hotel,
    HotelOperatingMetric,
    HotelOperatingStatement,
    UsaliDepartmentLine,
)
from app.infrastructure.postgres.session import session_scope


def _coerce_uuid(value: str | uuid.UUID | None) -> uuid.UUID | None:
    if value is None or isinstance(value, uuid.UUID):
        return value
    return uuid.UUID(str(value))


def _json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def model_to_dict(model: Any) -> dict[str, Any]:
    return {column.name: _json_value(getattr(model, column.name)) for column in model.__table__.columns}


def _clean_tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(token) > 2]


class PostgresDocumentRepository:
    def create(
        self,
        *,
        hotel_id: str | None,
        filename: str,
        original_filename: str,
        file_type: str,
        mime_type: str | None,
        storage_path: str,
    ) -> dict[str, Any]:
        with session_scope() as session:
            document = Document(
                hotel_id=_coerce_uuid(hotel_id),
                filename=filename,
                original_filename=original_filename,
                file_type=file_type,
                mime_type=mime_type,
                storage_path=storage_path,
                processing_status="uploaded",
            )
            session.add(document)
            session.flush()
            return model_to_dict(document)

    def get(self, document_id: str) -> dict[str, Any] | None:
        with session_scope() as session:
            document = session.get(Document, _coerce_uuid(document_id))
            return model_to_dict(document) if document else None

    def list(self) -> list[dict[str, Any]]:
        with session_scope() as session:
            rows = (
                session.execute(
                    select(Document, Hotel.name.label("hotel_name"))
                    .outerjoin(Hotel, Document.hotel_id == Hotel.id)
                    .order_by(Document.created_at.desc())
                )
                .all()
            )
            documents = []
            for document, hotel_name in rows:
                payload = model_to_dict(document)
                payload["hotel_name"] = hotel_name
                documents.append(payload)
            return documents

    def update_status(self, document_id: str, status: str, error_message: str | None = None) -> None:
        with session_scope() as session:
            document = session.get(Document, _coerce_uuid(document_id))
            if document:
                document.processing_status = status
                document.error_message = error_message
                document.updated_at = func.now()

    def update_parser(self, document_id: str, parser_name: str) -> None:
        with session_scope() as session:
            document = session.get(Document, _coerce_uuid(document_id))
            if document:
                document.parser_name = parser_name
                document.updated_at = func.now()

    def update_classification(
        self, document_id: str, document_type: str, confidence: float | None
    ) -> None:
        with session_scope() as session:
            document = session.get(Document, _coerce_uuid(document_id))
            if document:
                document.document_type = document_type
                document.classification_confidence = confidence
                document.updated_at = func.now()

    def set_hotel(self, document_id: str, hotel_id: str) -> None:
        with session_scope() as session:
            document = session.get(Document, _coerce_uuid(document_id))
            if document:
                document.hotel_id = _coerce_uuid(hotel_id)
                document.updated_at = func.now()


class PostgresHotelRepository:
    def create(self, values: dict[str, Any]) -> dict[str, Any]:
        with session_scope() as session:
            hotel = Hotel(**values)
            session.add(hotel)
            session.flush()
            return model_to_dict(hotel)

    def get(self, hotel_id: str) -> dict[str, Any] | None:
        with session_scope() as session:
            hotel = session.get(Hotel, _coerce_uuid(hotel_id))
            return model_to_dict(hotel) if hotel else None

    def list(self) -> list[dict[str, Any]]:
        with session_scope() as session:
            hotels = session.execute(select(Hotel).order_by(Hotel.created_at.desc())).scalars().all()
            return [model_to_dict(hotel) for hotel in hotels]

    def update_missing(self, hotel_id: str, values: dict[str, Any]) -> dict[str, Any] | None:
        with session_scope() as session:
            hotel = session.get(Hotel, _coerce_uuid(hotel_id))
            if not hotel:
                return None
            for key, value in values.items():
                if value is not None and getattr(hotel, key, None) is None:
                    setattr(hotel, key, value)
            hotel.updated_at = func.now()
            session.flush()
            return model_to_dict(hotel)

    def detail(self, hotel_id: str) -> dict[str, Any] | None:
        with session_scope() as session:
            hotel = session.get(Hotel, _coerce_uuid(hotel_id))
            if not hotel:
                return None

            documents = (
                session.execute(
                    select(Document)
                    .where(Document.hotel_id == hotel.id)
                    .order_by(Document.created_at.desc())
                )
                .scalars()
                .all()
            )
            statements = (
                session.execute(
                    select(HotelOperatingStatement)
                    .where(HotelOperatingStatement.hotel_id == hotel.id)
                    .order_by(HotelOperatingStatement.created_at.desc())
                )
                .scalars()
                .all()
            )
            statement_payloads = []
            for statement in statements:
                statement_payload = model_to_dict(statement)
                lines = (
                    session.execute(
                        select(UsaliDepartmentLine).where(
                            UsaliDepartmentLine.operating_statement_id == statement.id
                        )
                    )
                    .scalars()
                    .all()
                )
                metric = session.execute(
                    select(HotelOperatingMetric).where(
                        HotelOperatingMetric.operating_statement_id == statement.id
                    )
                ).scalar_one_or_none()
                statement_payload["department_lines"] = [model_to_dict(line) for line in lines]
                statement_payload["metrics"] = model_to_dict(metric) if metric else None
                statement_payloads.append(statement_payload)

            return {
                "hotel": model_to_dict(hotel),
                "documents": [model_to_dict(document) for document in documents],
                "operatingStatements": statement_payloads,
            }


class PostgresExtractionRepository:
    def create(
        self,
        *,
        document_id: str,
        extraction_type: str,
        raw_json: dict[str, Any],
        confidence: float | None,
    ) -> dict[str, Any]:
        with session_scope() as session:
            extraction = Extraction(
                document_id=_coerce_uuid(document_id),
                extraction_type=extraction_type,
                raw_json=raw_json,
                confidence=confidence,
            )
            session.add(extraction)
            session.flush()
            return model_to_dict(extraction)


class PostgresOperatingStatementRepository:
    def create_statement(
        self, *, hotel_id: str, document_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        with session_scope() as session:
            statement = HotelOperatingStatement(
                hotel_id=_coerce_uuid(hotel_id),
                document_id=_coerce_uuid(document_id),
                **values,
            )
            session.add(statement)
            session.flush()
            return model_to_dict(statement)

    def create_department_line(
        self, *, operating_statement_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        with session_scope() as session:
            line = UsaliDepartmentLine(
                operating_statement_id=_coerce_uuid(operating_statement_id), **values
            )
            session.add(line)
            session.flush()
            return model_to_dict(line)

    def create_metrics(
        self, *, operating_statement_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        with session_scope() as session:
            metric = HotelOperatingMetric(
                operating_statement_id=_coerce_uuid(operating_statement_id), **values
            )
            session.add(metric)
            session.flush()
            return model_to_dict(metric)

    def list_for_hotel(self, hotel_id: str) -> list[dict[str, Any]]:
        detail = PostgresHotelRepository().detail(hotel_id)
        return detail["operatingStatements"] if detail else []


class PostgresChunkRepository:
    def add_many(self, document_id: str, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        with session_scope() as session:
            rows = [
                DocumentChunk(document_id=_coerce_uuid(document_id), **chunk)
                for chunk in chunks
                if chunk.get("chunk_text")
            ]
            session.add_all(rows)
            session.flush()
            return [model_to_dict(row) for row in rows]

    def list_for_document(self, document_id: str) -> list[dict[str, Any]]:
        with session_scope() as session:
            chunks = (
                session.execute(
                    select(DocumentChunk)
                    .where(DocumentChunk.document_id == _coerce_uuid(document_id))
                    .order_by(DocumentChunk.chunk_index.asc())
                )
                .scalars()
                .all()
            )
            return [model_to_dict(chunk) for chunk in chunks]

    def search(self, document_id: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
        tokens = _clean_tokens(query)
        if not tokens:
            return []
        counts = Counter(tokens)
        chunks = self.list_for_document(document_id)
        scored = []
        for chunk in chunks:
            text = chunk["chunk_text"].lower()
            score = sum(text.count(token) * weight for token, weight in counts.items())
            if score:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]


class PostgresExtractedTableRepository:
    def add_many(self, document_id: str, tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
        with session_scope() as session:
            rows = [
                ExtractedTable(document_id=_coerce_uuid(document_id), **table)
                for table in tables
            ]
            session.add_all(rows)
            session.flush()
            return [model_to_dict(row) for row in rows]
