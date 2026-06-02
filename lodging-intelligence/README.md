# Lodging Intelligence

Lodging Intelligence is a local MVP for hotel and lodging document intelligence. It uploads lodging-related files, parses text and tables, stores canonical data in PostgreSQL, keeps raw extraction JSON in JSONB, supports document Q&A with citations, and exports hotel data to JSON or CSV.

The financial extraction is USALI-aligned. Licensed schedules, account dictionaries, and official mappings are intentionally out of scope for this MVP.

## Architecture Summary

- Frontend: Next.js, React, TypeScript
- Backend: FastAPI, Pydantic, SQLAlchemy
- Database: PostgreSQL
- Migrations: Alembic
- Storage: local filesystem through a storage service
- LLM: OpenAI API through an environment-configured client
- Retrieval: keyword chunk retrieval first; pgvector can be added behind the retrieval boundary later

API routes call services. Services contain workflow logic. PostgreSQL-specific persistence lives under `backend/app/infrastructure/postgres`.

## Local PostgreSQL Setup

This project assumes a local PostgreSQL database named lodging_intelligence already exists.

Example:

```bash
psql -U postgres -c "CREATE DATABASE lodging_intelligence;"
```

The application does not create the database itself. Alembic migrations create the schema inside the existing database.

Create a local `.env` in the project root from `.env.example` and update the password. The backend also supports `backend/.env` for local overrides.

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/lodging_intelligence
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
LOCAL_STORAGE_DIR=./storage
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Backend

The backend uses `uv` for dependency installation and command execution.

Install dependencies:

```bash
cd backend
uv sync --extra test
```

Run migrations:

```bash
cd backend
uv run alembic upgrade head
```

Start the API:

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests:

```bash
cd backend
uv run pytest
```

Tests use mocked OpenAI calls and do not require a real OpenAI API request.

## Frontend

Install dependencies:

```bash
cd frontend
npm install
```

Start the app:

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Uploading A Document

1. Start PostgreSQL and run `alembic upgrade head`.
2. Start the backend on port 8000.
3. Start the frontend on port 3000.
4. Go to `/upload`.
5. Upload a PDF, DOCX, XLSX, or CSV.

The backend stores the original file locally, creates a `documents` row, parses text and tables, creates chunks, classifies the document, stores raw extraction payloads in JSONB, and normalizes hotel and operating statement data when the source supports it.

## API Endpoints

- `POST /api/documents/upload`
- `GET /api/documents`
- `GET /api/documents/{document_id}`
- `GET /api/hotels`
- `GET /api/hotels/{hotel_id}`
- `POST /api/chat`
- `GET /api/hotels/{hotel_id}/export/json`
- `GET /api/hotels/{hotel_id}/export/csv`

## MVP Limitations

- No authentication, billing, or multi-tenancy.
- No Celery or Redis; upload processing uses FastAPI background tasks.
- No advanced OCR for scanned documents.
- No cloud object storage yet.
- No licensed USALI account dictionary.
- No valuation model, STR benchmarking engine, debt sizing, or investment memo generation.
- pgvector is not required for the first migration; keyword retrieval is implemented first.

## Future Improvements

- Add pgvector embeddings and semantic retrieval.
- Add human review and approval workflows for extracted values.
- Add cloud storage through the existing storage service boundary.
- Add richer spreadsheet table normalization.
- Add official licensed USALI schedules and mappings if the project scope later includes them.
