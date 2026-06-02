from __future__ import annotations

from app.infrastructure.parsers.base import DocumentParser
from app.infrastructure.parsers.csv_parser import CsvParser
from app.infrastructure.parsers.docx_parser import DocxParser
from app.infrastructure.parsers.pdf_parser import PdfParser
from app.infrastructure.parsers.xlsx_parser import XlsxParser


def get_parser(file_type: str) -> DocumentParser:
    parsers: dict[str, DocumentParser] = {
        "pdf": PdfParser(),
        "docx": DocxParser(),
        "xlsx": XlsxParser(),
        "csv": CsvParser(),
    }
    try:
        return parsers[file_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported parser file type: {file_type}") from exc
