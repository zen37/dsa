from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass
class ParsedPage:
    page_number: int | None
    text: str
    section_name: str | None = None
    sheet_name: str | None = None


@dataclass
class ParsedTable:
    source_name: str
    page_number: int | None
    sheet_name: str | None
    rows: list[dict[str, Any]]


@dataclass
class ParsedDocument:
    file_type: str
    pages: list[ParsedPage]
    tables: list[ParsedTable]
    metadata: dict[str, Any]


class DocumentParser(Protocol):
    file_type: str

    def parse(self, path: str | Path) -> ParsedDocument:
        ...


def rows_to_text(rows: list[dict[str, Any]], limit: int = 50) -> str:
    lines = []
    for row in rows[:limit]:
        cells = [f"{key}: {value}" for key, value in row.items() if value not in (None, "")]
        if cells:
            lines.append("; ".join(cells))
    return "\n".join(lines)
