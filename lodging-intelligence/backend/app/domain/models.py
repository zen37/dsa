from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_FILE_TYPES = {"pdf", "docx", "xlsx", "csv", "unknown"}
SUPPORTED_FILE_TYPES = {"pdf", "docx", "xlsx", "csv"}
ALLOWED_PROCESSING_STATUSES = {"uploaded", "processing", "processed", "failed"}
ALLOWED_DOCUMENT_TYPES = {
    "offering_memorandum",
    "profit_and_loss_statement",
    "operating_statement",
    "str_report",
    "budget_forecast",
    "appraisal",
    "capex_report",
    "management_agreement",
    "lease",
    "property_brochure",
    "brand_standard_document",
    "unknown",
}
ALLOWED_EXTRACTION_TYPES = {
    "document_summary",
    "property_profile",
    "operating_statement",
    "operating_metrics",
    "capex_items",
    "market_data",
    "unknown",
}
USALI_ALIGNED_DEPARTMENT_CODES = {
    "ROOMS",
    "FOOD_AND_BEVERAGE",
    "OTHER_OPERATED_DEPARTMENTS",
    "MISCELLANEOUS_INCOME",
    "ADMINISTRATIVE_AND_GENERAL",
    "INFORMATION_AND_TELECOMMUNICATIONS_SYSTEMS",
    "SALES_AND_MARKETING",
    "PROPERTY_OPERATIONS_AND_MAINTENANCE",
    "ENERGY_WATER_AND_WASTE",
    "MANAGEMENT_FEES",
    "NON_OPERATING_INCOME_EXPENSE",
    "UNKNOWN",
}


@dataclass(frozen=True)
class Citation:
    document_id: str
    page_number: int | None
    sheet_name: str | None
    section_name: str | None
    chunk_id: str


JsonDict = dict[str, Any]
