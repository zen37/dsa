from __future__ import annotations

from typing import Any

from app.domain.repositories import DocumentRepository, HotelRepository
from app.infrastructure.postgres.repositories import PostgresDocumentRepository, PostgresHotelRepository


PROFILE_FIELD_MAP = {
    "name": "name",
    "address": "address",
    "city": "city",
    "state": "state",
    "country": "country",
    "market": "market",
    "keys": "key_count",
    "brand": "brand",
    "management": "management_company",
    "ownershipInterest": "ownership_interest",
    "buildingAreaSqft": "building_area_sqft",
    "siteAreaAcres": "site_area_acres",
    "parkingSpaces": "parking_spaces",
}


def source_value(raw: dict[str, Any], key: str) -> Any:
    value = raw.get(key, {})
    return value.get("value") if isinstance(value, dict) else None


class HotelService:
    def __init__(
        self,
        hotel_repo: HotelRepository | None = None,
        document_repo: DocumentRepository | None = None,
    ) -> None:
        self.hotel_repo = hotel_repo or PostgresHotelRepository()
        self.document_repo = document_repo or PostgresDocumentRepository()

    def normalize_property_profile(
        self, *, document_id: str, hotel_id: str | None, profile: dict[str, Any]
    ) -> dict[str, Any] | None:
        hotel_raw = profile.get("hotel", {})
        values = {
            db_key: source_value(hotel_raw, extraction_key)
            for extraction_key, db_key in PROFILE_FIELD_MAP.items()
        }
        if hotel_id:
            hotel = self.hotel_repo.update_missing(hotel_id, values)
            self.document_repo.set_hotel(document_id, hotel_id)
            return hotel

        if not any(value is not None for value in values.values()):
            return None

        hotel = self.hotel_repo.create(values)
        self.document_repo.set_hotel(document_id, hotel["id"])
        return hotel

    def list_hotels(self) -> list[dict[str, Any]]:
        return self.hotel_repo.list()

    def get_hotel_detail(self, hotel_id: str) -> dict[str, Any] | None:
        return self.hotel_repo.detail(hotel_id)
