import Link from "next/link";
import DocumentStatus from "../../components/DocumentStatus";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type DocumentRow = {
  id: string;
  filename: string;
  file_type: string;
  document_type?: string | null;
  processing_status: string;
  created_at: string;
  hotel_id?: string | null;
  hotel_name?: string | null;
};

async function getDocuments(): Promise<DocumentRow[]> {
  const response = await fetch(`${apiBase}/api/documents`, { cache: "no-store" });
  if (!response.ok) return [];
  return response.json();
}

export default async function DocumentsPage() {
  const documents = await getDocuments();

  return (
    <section className="section">
      <div className="button-row" style={{ justifyContent: "space-between" }}>
        <h1>Documents</h1>
        <Link className="button" href="/upload">
          Upload
        </Link>
      </div>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Filename</th>
              <th>File type</th>
              <th>Document type</th>
              <th>Status</th>
              <th>Created</th>
              <th>Hotel</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((document) => (
              <tr key={document.id}>
                <td>
                  <Link href={`/documents/${document.id}/chat`}>{document.filename}</Link>
                </td>
                <td>{document.file_type}</td>
                <td>{document.document_type || "unknown"}</td>
                <td>
                  <DocumentStatus status={document.processing_status} />
                </td>
                <td>{new Date(document.created_at).toLocaleString()}</td>
                <td>
                  {document.hotel_id ? (
                    <Link href={`/hotels/${document.hotel_id}`}>
                      {document.hotel_name || "Hotel profile"}
                    </Link>
                  ) : (
                    "Not linked"
                  )}
                </td>
              </tr>
            ))}
            {!documents.length ? (
              <tr>
                <td colSpan={6}>No documents uploaded yet.</td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}
