from __future__ import annotations

from pathlib import Path
from typing import Any

from app.infrastructure.parsers.base import ParsedDocument, ParsedPage, ParsedTable


class PdfParser:
    file_type = "pdf"

    def parse(self, path: str | Path) -> ParsedDocument:
        import fitz

        path = Path(path)
        pages: list[ParsedPage] = []
        metadata: dict[str, Any] = {}

        with fitz.open(path) as doc:
            metadata = dict(doc.metadata or {})
            for index, page in enumerate(doc, start=1):
                pages.append(ParsedPage(page_number=index, text=page.get_text("text").strip()))

        tables: list[ParsedTable] = []
        try:
            import pdfplumber

            with pdfplumber.open(path) as pdf:
                for index, page in enumerate(pdf.pages, start=1):
                    for table_index, table in enumerate(page.extract_tables() or [], start=1):
                        if not table:
                            continue
                        headers = [
                            str(value).strip() if value not in (None, "") else f"column_{i + 1}"
                            for i, value in enumerate(table[0])
                        ]
                        rows = []
                        for row in table[1:]:
                            rows.append(
                                {
                                    headers[i] if i < len(headers) else f"column_{i + 1}": value
                                    for i, value in enumerate(row)
                                }
                            )
                        tables.append(
                            ParsedTable(
                                source_name=f"page_{index}_table_{table_index}",
                                page_number=index,
                                sheet_name=None,
                                rows=rows,
                            )
                        )
        except Exception:
            metadata["table_extraction_warning"] = "PDF table extraction was skipped or failed."

        return ParsedDocument(file_type=self.file_type, pages=pages, tables=tables, metadata=metadata)
