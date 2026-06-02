"use client";

import { FormEvent, useState } from "react";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type Citation = {
  document_id: string;
  page_number: number | null;
  sheet_name: string | null;
  section_name: string | null;
  chunk_id: string;
};

type ChatResponse = {
  answer: string;
  citations: Citation[];
};

export default function ChatPanel({ documentId }: { documentId: string }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError("");
    setAnswer(null);

    const response = await fetch(`${apiBase}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document_id: documentId, question })
    });

    setLoading(false);
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      setError(payload.detail || "Chat failed.");
      return;
    }

    setAnswer((await response.json()) as ChatResponse);
  }

  return (
    <section className="chat-layout">
      <form className="panel" onSubmit={submit}>
        <label htmlFor="question">
          <strong>Ask about this document</strong>
        </label>
        <textarea
          id="question"
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="What does the document say about parking?"
          value={question}
        />
        <button disabled={loading || !question.trim()} type="submit">
          {loading ? "Asking..." : "Ask"}
        </button>
        {error ? <p className="muted">{error}</p> : null}
      </form>
      {answer ? (
        <section className="panel">
          <h2>Answer</h2>
          <div className="answer">{answer.answer}</div>
          <h3>Citations</h3>
          <div className="citation-list">
            {answer.citations.length ? (
              answer.citations.map((citation) => (
                <div className="citation" key={citation.chunk_id}>
                  Page {citation.page_number || "n/a"} | Sheet {citation.sheet_name || "n/a"} |
                  Section {citation.section_name || "n/a"}
                </div>
              ))
            ) : (
              <p className="muted">No citations returned.</p>
            )}
          </div>
        </section>
      ) : null}
    </section>
  );
}
