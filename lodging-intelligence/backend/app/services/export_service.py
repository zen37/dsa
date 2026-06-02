from __future__ import annotations

from io import StringIO
import csv
from typing import Any

from app.domain.repositories import HotelRepository
from app.infrastructure.postgres.repositories import PostgresHotelRepository


CSV_COLUMNS = [
    "hotel_name",
    "address",
    "city",
    "state",
    "country",
    "market",
    "key_count",
    "brand",
    "management_company",
    "period_label",
    "currency",
    "rooms_revenue",
    "food_and_beverage_revenue",
    "other_revenue",
    "total_revenue",
    "gross_operating_profit",
    "ebitda",
    "net_operating_income",
    "occupancy",
    "adr",
    "revpar",
    "noi_per_key",
    "gop_margin",
]


class ExportService:
    def __init__(self, hotel_repo: HotelRepository | None = None) -> None:
        self.hotel_repo = hotel_repo or PostgresHotelRepository()

    def export_json(self, hotel_id: str) -> dict[str, Any] | None:
        detail = self.hotel_repo.detail(hotel_id)
        if not detail:
            return None
        metrics = [
            statement.get("metrics")
            for statement in detail.get("operatingStatements", [])
            if statement.get("metrics")
        ]
        return {
            "hotel": detail["hotel"],
            "documents": detail.get("documents", []),
            "operatingStatements": detail.get("operatingStatements", []),
            "metrics": metrics,
        }

    def export_csv(self, hotel_id: str) -> str | None:
        detail = self.hotel_repo.detail(hotel_id)
        if not detail:
            return None

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        hotel = detail["hotel"]
        statements = detail.get("operatingStatements") or [None]
        for statement in statements:
            metrics = (statement or {}).get("metrics") or {}
            row = {
                "hotel_name": hotel.get("name"),
                "address": hotel.get("address"),
                "city": hotel.get("city"),
                "state": hotel.get("state"),
                "country": hotel.get("country"),
                "market": hotel.get("market"),
                "key_count": hotel.get("key_count"),
                "brand": hotel.get("brand"),
                "management_company": hotel.get("management_company"),
                "period_label": (statement or {}).get("period_label"),
                "currency": (statement or {}).get("currency"),
                "rooms_revenue": (statement or {}).get("rooms_revenue"),
                "food_and_beverage_revenue": (statement or {}).get("food_and_beverage_revenue"),
                "other_revenue": (statement or {}).get("other_revenue"),
                "total_revenue": (statement or {}).get("total_revenue"),
                "gross_operating_profit": (statement or {}).get("gross_operating_profit"),
                "ebitda": (statement or {}).get("ebitda"),
                "net_operating_income": (statement or {}).get("net_operating_income"),
                "occupancy": metrics.get("occupancy"),
                "adr": metrics.get("adr"),
                "revpar": metrics.get("revpar"),
                "noi_per_key": metrics.get("noi_per_key"),
                "gop_margin": metrics.get("gop_margin"),
            }
            writer.writerow(row)
        return output.getvalue()
