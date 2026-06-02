"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type UploadResponse = {
  document_id: string;
  hotel_id: string | null;
  filename: string;
  file_type: string;
  processing_status: string;
};

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<UploadResponse | null>(null);
  const [status, setStatus] = useState<string>("");
  const [error, setError] = useState<string>("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) return;

    setStatus("Uploading...");
    setError("");
    setResult(null);

    const form = new FormData();
    form.append("file", file);

    const response = await fetch(`${apiBase}/api/documents/upload`, {
      method: "POST",
      body: form
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      setError(payload.detail || "Upload failed.");
      setStatus("");
      return;
    }

    const payload = (await response.json()) as UploadResponse;
    setResult(payload);
    setStatus("Uploaded. Background processing has started.");
  }

  return (
    <form className="upload-box" onSubmit={submit}>
      <strong>Upload a lodging document</strong>
      <p className="muted">Accepted file types: .pdf, .docx, .xlsx, .csv</p>
      <input
        accept=".pdf,.docx,.xlsx,.csv,application/pdf,text/csv,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        onChange={(event) => setFile(event.target.files?.[0] || null)}
        type="file"
      />
      <button disabled={!file} type="submit">
        Upload
      </button>
      {status ? <p>{status}</p> : null}
      {error ? <p className="muted">{error}</p> : null}
      {result ? (
        <div className="panel" style={{ marginTop: 16 }}>
          <p>
            <strong>{result.filename}</strong> is {result.processing_status}.
          </p>
          <div className="button-row">
            <Link className="button secondary" href={`/documents/${result.document_id}/chat`}>
              Open document chat
            </Link>
            <Link className="button secondary" href="/documents">
              View documents
            </Link>
          </div>
        </div>
      ) : null}
    </form>
  );
}
