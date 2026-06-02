from __future__ import annotations

from pathlib import Path
import csv

from app.infrastructure.parsers.base import ParsedDocument, ParsedPage, ParsedTable, rows_to_text


class CsvParser:
    file_type = "csv"

    def parse(self, path: str | Path) -> ParsedDocument:
        path = Path(path)
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            sample = handle.read(2048)
            handle.seek(0)
            dialect = csv.Sniffer().sniff(sample) if sample.strip() else csv.excel
            reader = csv.DictReader(handle, dialect=dialect)
            rows = [dict(row) for row in reader]

        table = ParsedTable(source_name=path.name, page_number=None, sheet_name=None, rows=rows)
        page = ParsedPage(page_number=None, text=rows_to_text(rows), section_name=path.name)
        return ParsedDocument(
            file_type=self.file_type,
            pages=[page],
            tables=[table],
            metadata={"row_count": len(rows)},
        )
