from __future__ import annotations

from app.infrastructure.parsers.base import ParsedDocument, rows_to_text


def split_text(text: str, max_chars: int = 1800, overlap: int = 150) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def build_chunks(parsed: ParsedDocument) -> list[dict]:
    chunks: list[dict] = []
    index = 0

    for page in parsed.pages:
        for text in split_text(page.text):
            chunks.append(
                {
                    "page_number": page.page_number,
                    "sheet_name": page.sheet_name,
                    "section_name": page.section_name,
                    "chunk_index": index,
                    "chunk_type": "sheet" if page.sheet_name else "page",
                    "chunk_text": text,
                }
            )
            index += 1

    for table in parsed.tables:
        table_text = rows_to_text(table.rows)
        for text in split_text(table_text):
            chunks.append(
                {
                    "page_number": table.page_number,
                    "sheet_name": table.sheet_name,
                    "section_name": table.source_name,
                    "chunk_index": index,
                    "chunk_type": "table",
                    "chunk_text": text,
                }
            )
            index += 1

    return chunks
