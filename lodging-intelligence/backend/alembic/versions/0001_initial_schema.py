"""Initial Lodging Intelligence schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-27
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.Text()),
        sa.Column("address", sa.Text()),
        sa.Column("city", sa.Text()),
        sa.Column("state", sa.Text()),
        sa.Column("country", sa.Text()),
        sa.Column("market", sa.Text()),
        sa.Column("key_count", sa.Integer()),
        sa.Column("brand", sa.Text()),
        sa.Column("management_company", sa.Text()),
        sa.Column("ownership_interest", sa.Text()),
        sa.Column("building_area_sqft", sa.Numeric()),
        sa.Column("site_area_acres", sa.Numeric()),
        sa.Column("parking_spaces", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("hotel_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("hotels.id")),
        sa.Column("filename", sa.Text(), nullable=False),
        sa.Column("original_filename", sa.Text(), nullable=False),
        sa.Column("file_type", sa.Text(), nullable=False),
        sa.Column("mime_type", sa.Text()),
        sa.Column("storage_path", sa.Text(), nullable=False),
        sa.Column("parser_name", sa.Text()),
        sa.Column("document_type", sa.Text()),
        sa.Column("classification_confidence", sa.Numeric()),
        sa.Column("processing_status", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "document_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("page_number", sa.Integer()),
        sa.Column("sheet_name", sa.Text()),
        sa.Column("section_name", sa.Text()),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_type", sa.Text(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "extracted_tables",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_name", sa.Text()),
        sa.Column("page_number", sa.Integer()),
        sa.Column("sheet_name", sa.Text()),
        sa.Column("table_index", sa.Integer()),
        sa.Column("raw_json", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "extractions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("extraction_type", sa.Text(), nullable=False),
        sa.Column("raw_json", postgresql.JSONB(), nullable=False),
        sa.Column("confidence", sa.Numeric()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "hotel_operating_statements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("hotel_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("hotels.id"), nullable=False),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("documents.id"),
            nullable=False,
        ),
        sa.Column("period_label", sa.Text()),
        sa.Column("currency", sa.Text(), server_default="USD"),
        sa.Column("total_revenue", sa.Numeric()),
        sa.Column("rooms_revenue", sa.Numeric()),
        sa.Column("food_and_beverage_revenue", sa.Numeric()),
        sa.Column("other_revenue", sa.Numeric()),
        sa.Column("gross_operating_profit", sa.Numeric()),
        sa.Column("ebitda", sa.Numeric()),
        sa.Column("net_operating_income", sa.Numeric()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "usali_department_lines",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "operating_statement_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("hotel_operating_statements.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("department_code", sa.Text(), nullable=False),
        sa.Column("department_name", sa.Text()),
        sa.Column("original_source_label", sa.Text()),
        sa.Column("revenue", sa.Numeric()),
        sa.Column("expenses", sa.Numeric()),
        sa.Column("departmental_profit", sa.Numeric()),
        sa.Column("confidence", sa.Numeric()),
        sa.Column("source_pages", postgresql.JSONB()),
        sa.Column("source_sheets", postgresql.JSONB()),
    )

    op.create_table(
        "hotel_operating_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "operating_statement_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("hotel_operating_statements.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("occupancy", sa.Numeric()),
        sa.Column("adr", sa.Numeric()),
        sa.Column("revpar", sa.Numeric()),
        sa.Column("available_rooms", sa.Integer()),
        sa.Column("occupied_rooms", sa.Integer()),
        sa.Column("noi_per_key", sa.Numeric()),
        sa.Column("gop_margin", sa.Numeric()),
    )


def downgrade() -> None:
    op.drop_table("hotel_operating_metrics")
    op.drop_table("usali_department_lines")
    op.drop_table("hotel_operating_statements")
    op.drop_table("extractions")
    op.drop_table("extracted_tables")
    op.drop_table("document_chunks")
    op.drop_table("documents")
    op.drop_table("hotels")
