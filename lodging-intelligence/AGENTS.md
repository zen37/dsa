# Agent Instructions

This project is Lodging Intelligence, a lodging document intelligence MVP.

Do not build a generic chatbot.

The app ingests lodging-related documents and extracts structured hotel/property/operating/financial data.

Use the required stack:
- Frontend: Next.js, React, TypeScript
- Backend: Python, FastAPI
- Database: PostgreSQL
- Migrations: Alembic
- ORM: SQLAlchemy

The local PostgreSQL database is named:

lodging_intelligence

The database is assumed to already exist. Do not create it from application code.

Use Alembic migrations to create/update tables.

Use PostgreSQL as the source of truth for canonical extracted data.

Use JSONB for raw extraction payloads.

Use local filesystem storage for original files in the MVP.

Keep PostgreSQL-specific code isolated in infrastructure/postgres.

API routes should call services.

Services should contain business logic.

Do not put SQLAlchemy session handling directly in API routes.

The MVP supports:
- PDF
- DOCX
- XLSX
- CSV

Use schema-first extraction.

Do not let the LLM invent facts.

Every extracted field should preserve source page, sheet, or section references where possible.

Financial extraction is USALI-aligned, not officially USALI-compliant.

Preserve original source labels for financial lines.

Do not discard unmapped financial lines.

Do not implement:
- Authentication
- Billing
- Multi-tenancy
- Oracle
- MongoDB
- SQL Server
- Celery
- Redis
- Advanced OCR
- Full official USALI compliance

Before finalizing changes:
1. Run backend tests if available.
2. Run frontend build/lint if available.
3. Update README when setup steps change.
