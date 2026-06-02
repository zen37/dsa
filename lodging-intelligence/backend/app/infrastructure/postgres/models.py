from __future__ import annotations

import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())


class Hotel(Base, TimestampMixin):
    __tablename__ = "hotels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(Text)
    state: Mapped[str | None] = mapped_column(Text)
    country: Mapped[str | None] = mapped_column(Text)
    market: Mapped[str | None] = mapped_column(Text)
    key_count: Mapped[int | None] = mapped_column(Integer)
    brand: Mapped[str | None] = mapped_column(Text)
    management_company: Mapped[str | None] = mapped_column(Text)
    ownership_interest: Mapped[str | None] = mapped_column(Text)
    building_area_sqft: Mapped[object | None] = mapped_column(Numeric)
    site_area_acres: Mapped[object | None] = mapped_column(Numeric)
    parking_spaces: Mapped[int | None] = mapped_column(Integer)

    documents: Mapped[list[Document]] = relationship(back_populates="hotel")
    operating_statements: Mapped[list[HotelOperatingStatement]] = relationship(back_populates="hotel")


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("hotels.id"))
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    original_filename: Mapped[str] = mapped_column(Text, nullable=False)
    file_type: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str | None] = mapped_column(Text)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    parser_name: Mapped[str | None] = mapped_column(Text)
    document_type: Mapped[str | None] = mapped_column(Text)
    classification_confidence: Mapped[object | None] = mapped_column(Numeric)
    processing_status: Mapped[str] = mapped_column(Text, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)

    hotel: Mapped[Hotel | None] = relationship(back_populates="documents")
    chunks: Mapped[list[DocumentChunk]] = relationship(back_populates="document", cascade="all, delete")
    extracted_tables: Mapped[list[ExtractedTable]] = relationship(
        back_populates="document", cascade="all, delete"
    )
    extractions: Mapped[list[Extraction]] = relationship(back_populates="document", cascade="all, delete")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    page_number: Mapped[int | None] = mapped_column(Integer)
    sheet_name: Mapped[str | None] = mapped_column(Text)
    section_name: Mapped[str | None] = mapped_column(Text)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_type: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())

    document: Mapped[Document] = relationship(back_populates="chunks")


class ExtractedTable(Base):
    __tablename__ = "extracted_tables"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    source_name: Mapped[str | None] = mapped_column(Text)
    page_number: Mapped[int | None] = mapped_column(Integer)
    sheet_name: Mapped[str | None] = mapped_column(Text)
    table_index: Mapped[int | None] = mapped_column(Integer)
    raw_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())

    document: Mapped[Document] = relationship(back_populates="extracted_tables")


class Extraction(Base):
    __tablename__ = "extractions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    extraction_type: Mapped[str] = mapped_column(Text, nullable=False)
    raw_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[object | None] = mapped_column(Numeric)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())

    document: Mapped[Document] = relationship(back_populates="extractions")


class HotelOperatingStatement(Base):
    __tablename__ = "hotel_operating_statements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("hotels.id"), nullable=False)
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False
    )
    period_label: Mapped[str | None] = mapped_column(Text)
    currency: Mapped[str | None] = mapped_column(Text, server_default="USD")
    total_revenue: Mapped[object | None] = mapped_column(Numeric)
    rooms_revenue: Mapped[object | None] = mapped_column(Numeric)
    food_and_beverage_revenue: Mapped[object | None] = mapped_column(Numeric)
    other_revenue: Mapped[object | None] = mapped_column(Numeric)
    gross_operating_profit: Mapped[object | None] = mapped_column(Numeric)
    ebitda: Mapped[object | None] = mapped_column(Numeric)
    net_operating_income: Mapped[object | None] = mapped_column(Numeric)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.now())

    hotel: Mapped[Hotel] = relationship(back_populates="operating_statements")
    department_lines: Mapped[list[UsaliDepartmentLine]] = relationship(
        back_populates="operating_statement", cascade="all, delete"
    )
    metrics: Mapped[HotelOperatingMetric | None] = relationship(
        back_populates="operating_statement", cascade="all, delete"
    )


class UsaliDepartmentLine(Base):
    __tablename__ = "usali_department_lines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operating_statement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hotel_operating_statements.id", ondelete="CASCADE"),
        nullable=False,
    )
    department_code: Mapped[str] = mapped_column(Text, nullable=False)
    department_name: Mapped[str | None] = mapped_column(Text)
    original_source_label: Mapped[str | None] = mapped_column(Text)
    revenue: Mapped[object | None] = mapped_column(Numeric)
    expenses: Mapped[object | None] = mapped_column(Numeric)
    departmental_profit: Mapped[object | None] = mapped_column(Numeric)
    confidence: Mapped[object | None] = mapped_column(Numeric)
    source_pages: Mapped[list | None] = mapped_column(JSONB)
    source_sheets: Mapped[list | None] = mapped_column(JSONB)

    operating_statement: Mapped[HotelOperatingStatement] = relationship(back_populates="department_lines")


class HotelOperatingMetric(Base):
    __tablename__ = "hotel_operating_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operating_statement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hotel_operating_statements.id", ondelete="CASCADE"),
        nullable=False,
    )
    occupancy: Mapped[object | None] = mapped_column(Numeric)
    adr: Mapped[object | None] = mapped_column(Numeric)
    revpar: Mapped[object | None] = mapped_column(Numeric)
    available_rooms: Mapped[int | None] = mapped_column(Integer)
    occupied_rooms: Mapped[int | None] = mapped_column(Integer)
    noi_per_key: Mapped[object | None] = mapped_column(Numeric)
    gop_margin: Mapped[object | None] = mapped_column(Numeric)

    operating_statement: Mapped[HotelOperatingStatement] = relationship(back_populates="metrics")
