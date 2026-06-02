from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.routes.documents import UnsupportedFileType
from app.main import app


class FakeDocumentService:
    def __init__(self) -> None:
        self.processed: list[str] = []

    async def upload(self, *, upload_file, hotel_id=None):
        suffix = (upload_file.filename or "").split(".")[-1].lower()
        if suffix not in {"pdf", "docx", "xlsx", "csv"}:
            raise UnsupportedFileType("Supported file types are PDF, DOCX, XLSX, and CSV.")
        return {
            "id": f"{suffix}-document-id",
            "hotel_id": hotel_id,
            "filename": upload_file.filename,
            "file_type": suffix,
            "processing_status": "uploaded",
        }

    def process_document(self, document_id: str) -> None:
        self.processed.append(document_id)


def install_fake_service(monkeypatch) -> FakeDocumentService:
    service = FakeDocumentService()
    monkeypatch.setattr("app.api.routes.documents.get_document_service", lambda: service)
    return service


def test_uploading_pdf_creates_document_row(monkeypatch):
    install_fake_service(monkeypatch)
    client = TestClient(app)
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.pdf", b"%PDF-1.4", "application/pdf")},
    )
    assert response.status_code == 201
    assert response.json()["file_type"] == "pdf"


def test_uploading_docx_creates_document_row(monkeypatch):
    install_fake_service(monkeypatch)
    client = TestClient(app)
    response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "sample.docx",
                b"docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )
    assert response.status_code == 201
    assert response.json()["file_type"] == "docx"


def test_uploading_xlsx_creates_document_row(monkeypatch):
    install_fake_service(monkeypatch)
    client = TestClient(app)
    response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "sample.xlsx",
                b"xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 201
    assert response.json()["file_type"] == "xlsx"


def test_uploading_csv_creates_document_row(monkeypatch):
    install_fake_service(monkeypatch)
    client = TestClient(app)
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.csv", b"name,keys\nHotel,100", "text/csv")},
    )
    assert response.status_code == 201
    assert response.json()["file_type"] == "csv"


def test_unsupported_file_types_are_rejected(monkeypatch):
    install_fake_service(monkeypatch)
    client = TestClient(app)
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.txt", b"not supported", "text/plain")},
    )
    assert response.status_code == 400
