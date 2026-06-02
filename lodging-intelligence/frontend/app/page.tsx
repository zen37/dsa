import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <section className="hero">
        <h1>Lodging Intelligence</h1>
        <p>
          Upload hotel and lodging documents, extract structured property and operating data,
          search the source content, and export the results.
        </p>
        <div className="actions">
          <Link className="button" href="/upload">
            Upload document
          </Link>
          <Link className="button secondary" href="/documents">
            View documents
          </Link>
        </div>
      </section>
      <section className="grid">
        <div className="card">
          <span className="label">Supported files</span>
          <div className="value">PDF, DOCX, XLSX, CSV</div>
        </div>
        <div className="card">
          <span className="label">Extraction focus</span>
          <div className="value">Profiles, metrics, USALI-aligned financials</div>
        </div>
        <div className="card">
          <span className="label">Source of truth</span>
          <div className="value">PostgreSQL</div>
        </div>
      </section>
    </>
  );
}
