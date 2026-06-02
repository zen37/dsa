from __future__ import annotations

import csv

from app.infrastructure.parsers.base import ParsedDocument, ParsedPage, ParsedTable
from app.infrastructure.retrieval.basic_retrieval import BasicRetrievalService
from app.services.chat_service import NOT_ENOUGH_INFORMATION, ChatService
from app.services.chunking import build_chunks, split_text
from app.services.classification_service import ClassificationService
from app.services.export_service import CSV_COLUMNS, ExportService
from app.services.extraction_service import ExtractionService
from app.services.hotel_service import HotelService
from app.services.operating_statement_service import OperatingStatementService


class FakeLLM:
    def __init__(self, json_payload=None, text_payload="Grounded answer.") -> None:
        self.json_payload = json_payload or {}
        self.text_payload = text_payload

    def json_chat(self, *, system: str, user: str):
        return self.json_payload

    def text_chat(self, *, system: str, user: str):
        return self.text_payload


def test_chunking_works_for_text():
    chunks = split_text(" ".join(f"word-{index}" for index in range(400)), max_chars=1000, overlap=100)
    assert len(chunks) > 1
    assert chunks[0] != chunks[1]


def test_chunking_works_for_tables():
    parsed = ParsedDocument(
        file_type="xlsx",
        pages=[],
        tables=[
            ParsedTable(
                source_name="Sheet1_table_1",
                page_number=None,
                sheet_name="Sheet1",
                rows=[{"Line": "Rooms Revenue", "Amount": 100}],
            )
        ],
        metadata={},
    )
    chunks = build_chunks(parsed)
    assert chunks[0]["chunk_type"] == "table"
    assert chunks[0]["sheet_name"] == "Sheet1"


def test_classification_returns_valid_document_type():
    service = ClassificationService(
        llm=FakeLLM(
            {
                "document_type": "offering_memorandum",
                "confidence": 0.94,
                "detected_sections": ["Executive Summary"],
            }
        )
    )
    result = service.classify("Executive Summary\nProperty Overview")
    assert result.document_type == "offering_memorandum"


def test_low_confidence_classification_returns_unknown():
    service = ClassificationService(
        llm=FakeLLM({"document_type": "appraisal", "confidence": 0.2, "detected_sections": []})
    )
    result = service.classify("thin context")
    assert result.document_type == "unknown"


def test_raw_extraction_payload_can_be_validated_and_stored():
    payload = {
        "hotel": {
            "name": {"value": "Example Hotel", "source_pages": [1], "source_sheets": []}
        },
        "confidence": 0.9,
    }
    service = ExtractionService(llm=FakeLLM(payload))
    extraction = service.extract_property_profile("context").model_dump()
    assert extraction["hotel"]["name"]["value"] == "Example Hotel"
    assert extraction["confidence"] == 0.9


class FakeHotelRepo:
    def __init__(self) -> None:
        self.hotels = {}
        self.created = None

    def create(self, values):
        self.created = values
        hotel = {"id": "hotel-1", **values}
        self.hotels["hotel-1"] = hotel
        return hotel

    def update_missing(self, hotel_id, values):
        hotel = self.hotels.setdefault(hotel_id, {"id": hotel_id, "name": "Existing"})
        for key, value in values.items():
            if value is not None and hotel.get(key) is None:
                hotel[key] = value
        return hotel

    def list(self):
        return list(self.hotels.values())

    def detail(self, hotel_id):
        return self.hotels.get(hotel_id)

    def get(self, hotel_id):
        return self.hotels.get(hotel_id)


class FakeDocumentRepo:
    def __init__(self) -> None:
        self.linked = None

    def set_hotel(self, document_id, hotel_id):
        self.linked = (document_id, hotel_id)


def test_property_profile_normalization_creates_hotel():
    hotel_repo = FakeHotelRepo()
    document_repo = FakeDocumentRepo()
    service = HotelService(hotel_repo=hotel_repo, document_repo=document_repo)
    profile = {
        "hotel": {
            "name": {"value": "Example Hotel"},
            "keys": {"value": 132},
            "market": {"value": "Miami Beach"},
        }
    }

    hotel = service.normalize_property_profile(
        document_id="doc-1", hotel_id=None, profile=profile
    )

    assert hotel["name"] == "Example Hotel"
    assert hotel["key_count"] == 132
    assert document_repo.linked == ("doc-1", "hotel-1")


def test_property_profile_normalization_updates_missing_fields_only():
    hotel_repo = FakeHotelRepo()
    hotel_repo.hotels["hotel-1"] = {"id": "hotel-1", "name": "Existing", "market": None}
    service = HotelService(hotel_repo=hotel_repo, document_repo=FakeDocumentRepo())
    profile = {
        "hotel": {
            "name": {"value": "New Name"},
            "market": {"value": "Seattle"},
        }
    }

    hotel = service.normalize_property_profile(
        document_id="doc-1", hotel_id="hotel-1", profile=profile
    )

    assert hotel["name"] == "Existing"
    assert hotel["market"] == "Seattle"


class FakeOperatingRepo:
    def __init__(self) -> None:
        self.statements = []
        self.lines = []
        self.metrics = []

    def create_statement(self, *, hotel_id, document_id, values):
        statement = {"id": "statement-1", "hotel_id": hotel_id, "document_id": document_id, **values}
        self.statements.append(statement)
        return statement

    def create_department_line(self, *, operating_statement_id, values):
        line = {"operating_statement_id": operating_statement_id, **values}
        self.lines.append(line)
        return line

    def create_metrics(self, *, operating_statement_id, values):
        metric = {"operating_statement_id": operating_statement_id, **values}
        self.metrics.append(metric)
        return metric

    def list_for_hotel(self, hotel_id):
        return self.statements


def test_usali_aligned_extraction_preserves_original_source_labels():
    repo = FakeOperatingRepo()
    service = OperatingStatementService(repo=repo)
    service.normalize(
        hotel_id="hotel-1",
        document_id="doc-1",
        extraction={
            "period": "2025",
            "currency": "USD",
            "summary": {"roomsRevenue": {"value": 100, "source_pages": [2]}},
            "metrics": {},
            "departmentLines": [
                {
                    "departmentCode": "ROOMS",
                    "departmentName": "Rooms",
                    "originalSourceLabel": "Rooms Revenue",
                    "revenue": {"value": 100, "source_pages": [2], "source_sheets": []},
                    "expenses": {"value": None, "source_pages": [], "source_sheets": []},
                    "departmentalProfit": {"value": None, "source_pages": [], "source_sheets": []},
                    "confidence": 0.9,
                }
            ],
        },
    )
    assert repo.lines[0]["original_source_label"] == "Rooms Revenue"
    assert repo.lines[0]["source_pages"] == [2]


def test_unmapped_financial_lines_are_stored_instead_of_discarded():
    repo = FakeOperatingRepo()
    service = OperatingStatementService(repo=repo)
    service.normalize(
        hotel_id="hotel-1",
        document_id="doc-1",
        extraction={
            "summary": {},
            "metrics": {},
            "departmentLines": [],
            "unmappedLines": [
                {
                    "originalSourceLabel": "Mystery Income",
                    "value": 55,
                    "source_pages": [5],
                    "source_sheets": [],
                }
            ],
        },
    )
    assert repo.lines[0]["department_code"] == "UNKNOWN"
    assert repo.lines[0]["original_source_label"] == "Mystery Income"


class FakeExportRepo:
    def detail(self, hotel_id):
        return {
            "hotel": {
                "id": hotel_id,
                "name": "Example Hotel",
                "address": "1 Main",
                "city": "Miami",
                "state": "FL",
                "country": "US",
                "market": "Miami",
                "key_count": 100,
                "brand": "Independent",
                "management_company": "Example Mgmt",
            },
            "documents": [{"id": "doc-1"}],
            "operatingStatements": [
                {
                    "id": "statement-1",
                    "period_label": "2025",
                    "currency": "USD",
                    "rooms_revenue": 10,
                    "food_and_beverage_revenue": 20,
                    "other_revenue": 5,
                    "total_revenue": 35,
                    "gross_operating_profit": 12,
                    "ebitda": 8,
                    "net_operating_income": 7,
                    "metrics": {"occupancy": 0.8, "adr": 250, "revpar": 200},
                }
            ],
        }


def test_export_json_returns_expected_shape():
    payload = ExportService(hotel_repo=FakeExportRepo()).export_json("hotel-1")
    assert sorted(payload.keys()) == ["documents", "hotel", "metrics", "operatingStatements"]
    assert payload["metrics"][0]["revpar"] == 200


def test_export_csv_returns_expected_columns():
    payload = ExportService(hotel_repo=FakeExportRepo()).export_csv("hotel-1")
    header = next(csv.reader(payload.splitlines()))
    assert header == CSV_COLUMNS


class FakeChunkRepo:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, document_id, query, limit=5):
        return self.chunks[:limit]


def test_chat_citations_work_for_pdf_page_numbers():
    retrieval = BasicRetrievalService(
        chunk_repo=FakeChunkRepo(
            [
                {
                    "id": "chunk-1",
                    "page_number": 20,
                    "sheet_name": None,
                    "section_name": None,
                    "chunk_text": "Parking includes 100 spaces.",
                }
            ]
        )
    )
    response = ChatService(retrieval_service=retrieval, llm=FakeLLM(text_payload="100 spaces.")).answer(
        document_id="doc-1", question="What about parking?"
    )
    assert response["citations"][0]["page_number"] == 20


def test_chat_citations_work_for_excel_sheet_names():
    retrieval = BasicRetrievalService(
        chunk_repo=FakeChunkRepo(
            [
                {
                    "id": "chunk-1",
                    "page_number": None,
                    "sheet_name": "Operating Statement",
                    "section_name": "Operating Statement",
                    "chunk_text": "RevPAR: 201.51",
                }
            ]
        )
    )
    response = ChatService(retrieval_service=retrieval, llm=FakeLLM(text_payload="RevPAR is 201.51.")).answer(
        document_id="doc-1", question="What is RevPAR?"
    )
    assert response["citations"][0]["sheet_name"] == "Operating Statement"


def test_chat_refuses_to_invent_when_no_relevant_chunks_are_found():
    retrieval = BasicRetrievalService(chunk_repo=FakeChunkRepo([]))
    response = ChatService(retrieval_service=retrieval, llm=FakeLLM()).answer(
        document_id="doc-1", question="What is the pool size?"
    )
    assert response["answer"] == NOT_ENOUGH_INFORMATION
    assert response["citations"] == []
