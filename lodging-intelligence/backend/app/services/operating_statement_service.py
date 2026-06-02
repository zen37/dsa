from __future__ import annotations

from typing import Any

from app.domain.models import USALI_ALIGNED_DEPARTMENT_CODES
from app.domain.repositories import OperatingStatementRepository
from app.infrastructure.postgres.repositories import PostgresOperatingStatementRepository


SUMMARY_FIELD_MAP = {
    "totalRevenue": "total_revenue",
    "roomsRevenue": "rooms_revenue",
    "foodAndBeverageRevenue": "food_and_beverage_revenue",
    "otherRevenue": "other_revenue",
    "grossOperatingProfit": "gross_operating_profit",
    "ebitda": "ebitda",
    "netOperatingIncome": "net_operating_income",
}


def value_of(raw: Any) -> Any:
    return raw.get("value") if isinstance(raw, dict) else None


def pages_of(*raw_values: Any) -> list[int]:
    pages: list[int] = []
    for raw in raw_values:
        if isinstance(raw, dict):
            pages.extend(raw.get("source_pages") or [])
    return sorted(set(pages))


def sheets_of(*raw_values: Any) -> list[str]:
    sheets: list[str] = []
    for raw in raw_values:
        if isinstance(raw, dict):
            sheets.extend(raw.get("source_sheets") or [])
    return sorted(set(sheets))


class OperatingStatementService:
    def __init__(self, repo: OperatingStatementRepository | None = None) -> None:
        self.repo = repo or PostgresOperatingStatementRepository()

    def normalize(
        self, *, hotel_id: str | None, document_id: str, extraction: dict[str, Any]
    ) -> dict[str, Any] | None:
        if not hotel_id:
            return None

        summary = extraction.get("summary") or {}
        statement_values = {
            db_key: value_of(summary.get(extraction_key))
            for extraction_key, db_key in SUMMARY_FIELD_MAP.items()
        }
        statement_values["period_label"] = extraction.get("period")
        statement_values["currency"] = extraction.get("currency") or "USD"

        if not any(value is not None for key, value in statement_values.items() if key != "currency"):
            if not extraction.get("departmentLines") and not extraction.get("unmappedLines"):
                return None

        statement = self.repo.create_statement(
            hotel_id=hotel_id, document_id=document_id, values=statement_values
        )

        metrics = extraction.get("metrics") or {}
        self.repo.create_metrics(
            operating_statement_id=statement["id"],
            values={
                "occupancy": value_of(metrics.get("occupancy")),
                "adr": value_of(metrics.get("adr")),
                "revpar": value_of(metrics.get("revpar")),
                "available_rooms": value_of(metrics.get("availableRooms")),
                "occupied_rooms": value_of(metrics.get("occupiedRooms")),
                "noi_per_key": value_of(metrics.get("noiPerKey")),
                "gop_margin": value_of(metrics.get("gopMargin")),
            },
        )

        for line in extraction.get("departmentLines") or []:
            revenue = line.get("revenue")
            expenses = line.get("expenses")
            departmental_profit = line.get("departmentalProfit")
            department_code = line.get("departmentCode") or "UNKNOWN"
            if department_code not in USALI_ALIGNED_DEPARTMENT_CODES:
                department_code = "UNKNOWN"
            self.repo.create_department_line(
                operating_statement_id=statement["id"],
                values={
                    "department_code": department_code,
                    "department_name": line.get("departmentName"),
                    "original_source_label": line.get("originalSourceLabel"),
                    "revenue": value_of(revenue),
                    "expenses": value_of(expenses),
                    "departmental_profit": value_of(departmental_profit),
                    "confidence": line.get("confidence"),
                    "source_pages": pages_of(revenue, expenses, departmental_profit),
                    "source_sheets": sheets_of(revenue, expenses, departmental_profit),
                },
            )

        for line in extraction.get("unmappedLines") or []:
            self.repo.create_department_line(
                operating_statement_id=statement["id"],
                values={
                    "department_code": "UNKNOWN",
                    "department_name": "Unmapped",
                    "original_source_label": line.get("originalSourceLabel"),
                    "revenue": line.get("value"),
                    "expenses": None,
                    "departmental_profit": None,
                    "confidence": None,
                    "source_pages": line.get("source_pages") or [],
                    "source_sheets": line.get("source_sheets") or [],
                },
            )

        return statement
