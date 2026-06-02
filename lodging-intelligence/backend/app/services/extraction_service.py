from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.infrastructure.llm.openai_client import OpenAIClient


class SourceValue(BaseModel):
    value: Any = None
    source_pages: list[int] = Field(default_factory=list)
    source_sheets: list[str] = Field(default_factory=list)


class SummaryExtraction(BaseModel):
    summary: SourceValue = Field(default_factory=SourceValue)
    key_points: list[SourceValue] = Field(default_factory=list)
    confidence: float = 0.0


class PropertyHotel(BaseModel):
    name: SourceValue = Field(default_factory=SourceValue)
    address: SourceValue = Field(default_factory=SourceValue)
    city: SourceValue = Field(default_factory=SourceValue)
    state: SourceValue = Field(default_factory=SourceValue)
    country: SourceValue = Field(default_factory=SourceValue)
    market: SourceValue = Field(default_factory=SourceValue)
    keys: SourceValue = Field(default_factory=SourceValue)
    brand: SourceValue = Field(default_factory=SourceValue)
    management: SourceValue = Field(default_factory=SourceValue)
    ownershipInterest: SourceValue = Field(default_factory=SourceValue)
    buildingAreaSqft: SourceValue = Field(default_factory=SourceValue)
    siteAreaAcres: SourceValue = Field(default_factory=SourceValue)
    parkingSpaces: SourceValue = Field(default_factory=SourceValue)


class PropertyProfileExtraction(BaseModel):
    hotel: PropertyHotel = Field(default_factory=PropertyHotel)
    confidence: float = 0.0


class DepartmentLineExtraction(BaseModel):
    departmentCode: str = "UNKNOWN"
    departmentName: str | None = None
    originalSourceLabel: str | None = None
    revenue: SourceValue = Field(default_factory=SourceValue)
    expenses: SourceValue = Field(default_factory=SourceValue)
    departmentalProfit: SourceValue = Field(default_factory=SourceValue)
    confidence: float = 0.0


class OperatingStatementExtraction(BaseModel):
    reportType: str = "usali_aligned_operating_statement"
    usaliComplianceLevel: str = "aligned_not_compliant"
    period: str | None = None
    currency: str = "USD"
    metrics: dict[str, SourceValue] = Field(default_factory=dict)
    summary: dict[str, SourceValue] = Field(default_factory=dict)
    departmentLines: list[DepartmentLineExtraction] = Field(default_factory=list)
    unmappedLines: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float = 0.0


class ExtractionService:
    def __init__(self, llm: OpenAIClient | None = None) -> None:
        self.llm = llm or OpenAIClient()

    def extract_summary(self, context: str) -> SummaryExtraction:
        raw = self.llm.json_chat(
            system=(
                "You extract lodging document summaries. Return only JSON. "
                "Extract only supported facts and preserve source pages or sheets."
            ),
            user=f"""
Return JSON with this exact shape:
{{
  "summary": {{"value": "string or null", "source_pages": [], "source_sheets": []}},
  "key_points": [
    {{"value": "string", "source_pages": [], "source_sheets": []}}
  ],
  "confidence": 0.0
}}

Document context:
{context[:12000]}
""",
        )
        return SummaryExtraction.model_validate(raw)

    def extract_property_profile(self, context: str) -> PropertyProfileExtraction:
        raw = self.llm.json_chat(
            system=(
                "You extract hotel property profile data from lodging documents. "
                "Return only JSON. Return null for fields that are not found."
            ),
            user=f"""
Return JSON with this exact shape:
{{
  "hotel": {{
    "name": {{"value": null, "source_pages": [], "source_sheets": []}},
    "address": {{"value": null, "source_pages": [], "source_sheets": []}},
    "city": {{"value": null, "source_pages": [], "source_sheets": []}},
    "state": {{"value": null, "source_pages": [], "source_sheets": []}},
    "country": {{"value": null, "source_pages": [], "source_sheets": []}},
    "market": {{"value": null, "source_pages": [], "source_sheets": []}},
    "keys": {{"value": null, "source_pages": [], "source_sheets": []}},
    "brand": {{"value": null, "source_pages": [], "source_sheets": []}},
    "management": {{"value": null, "source_pages": [], "source_sheets": []}},
    "ownershipInterest": {{"value": null, "source_pages": [], "source_sheets": []}},
    "buildingAreaSqft": {{"value": null, "source_pages": [], "source_sheets": []}},
    "siteAreaAcres": {{"value": null, "source_pages": [], "source_sheets": []}},
    "parkingSpaces": {{"value": null, "source_pages": [], "source_sheets": []}}
  }},
  "confidence": 0.0
}}

Document context:
{context[:12000]}
""",
        )
        return PropertyProfileExtraction.model_validate(raw)

    def extract_operating_statement(self, context: str) -> OperatingStatementExtraction:
        raw = self.llm.json_chat(
            system=(
                "You extract USALI-aligned lodging operating statement data. "
                "Do not claim official USALI compliance. Preserve original source labels. "
                "Use UNKNOWN for uncertain department mappings and keep unmapped lines."
            ),
            user=f"""
Return JSON shaped as:
{{
  "reportType": "usali_aligned_operating_statement",
  "usaliComplianceLevel": "aligned_not_compliant",
  "period": null,
  "currency": "USD",
  "metrics": {{
    "occupancy": {{"value": null, "source_pages": [], "source_sheets": []}},
    "adr": {{"value": null, "source_pages": [], "source_sheets": []}},
    "revpar": {{"value": null, "source_pages": [], "source_sheets": []}}
  }},
  "summary": {{
    "totalRevenue": {{"value": null, "source_pages": [], "source_sheets": []}},
    "roomsRevenue": {{"value": null, "source_pages": [], "source_sheets": []}},
    "foodAndBeverageRevenue": {{"value": null, "source_pages": [], "source_sheets": []}},
    "otherRevenue": {{"value": null, "source_pages": [], "source_sheets": []}},
    "grossOperatingProfit": {{"value": null, "source_pages": [], "source_sheets": []}},
    "ebitda": {{"value": null, "source_pages": [], "source_sheets": []}},
    "netOperatingIncome": {{"value": null, "source_pages": [], "source_sheets": []}}
  }},
  "departmentLines": [],
  "unmappedLines": [],
  "confidence": 0.0
}}

Document context:
{context[:14000]}
""",
        )
        return OperatingStatementExtraction.model_validate(raw)
