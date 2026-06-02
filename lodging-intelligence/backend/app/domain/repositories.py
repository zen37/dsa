from __future__ import annotations

from typing import Any, Protocol


class DocumentRepository(Protocol):
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
        ...

    def get(self, document_id: str) -> dict[str, Any] | None:
        ...

    def list(self) -> list[dict[str, Any]]:
        ...

    def update_status(self, document_id: str, status: str, error_message: str | None = None) -> None:
        ...

    def update_parser(self, document_id: str, parser_name: str) -> None:
        ...

    def update_classification(
        self, document_id: str, document_type: str, confidence: float | None
    ) -> None:
        ...

    def set_hotel(self, document_id: str, hotel_id: str) -> None:
        ...


class HotelRepository(Protocol):
    def create(self, values: dict[str, Any]) -> dict[str, Any]:
        ...

    def get(self, hotel_id: str) -> dict[str, Any] | None:
        ...

    def list(self) -> list[dict[str, Any]]:
        ...

    def update_missing(self, hotel_id: str, values: dict[str, Any]) -> dict[str, Any] | None:
        ...

    def detail(self, hotel_id: str) -> dict[str, Any] | None:
        ...


class ExtractionRepository(Protocol):
    def create(
        self,
        *,
        document_id: str,
        extraction_type: str,
        raw_json: dict[str, Any],
        confidence: float | None,
    ) -> dict[str, Any]:
        ...


class OperatingStatementRepository(Protocol):
    def create_statement(
        self, *, hotel_id: str, document_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        ...

    def create_department_line(
        self, *, operating_statement_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        ...

    def create_metrics(
        self, *, operating_statement_id: str, values: dict[str, Any]
    ) -> dict[str, Any]:
        ...

    def list_for_hotel(self, hotel_id: str) -> list[dict[str, Any]]:
        ...


class ChunkRepository(Protocol):
    def add_many(self, document_id: str, chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ...

    def list_for_document(self, document_id: str) -> list[dict[str, Any]]:
        ...

    def search(self, document_id: str, query: str, limit: int = 5) -> list[dict[str, Any]]:
        ...


class ExtractedTableRepository(Protocol):
    def add_many(self, document_id: str, tables: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ...
