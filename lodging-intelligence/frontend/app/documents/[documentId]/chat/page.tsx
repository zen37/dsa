import ChatPanel from "../../../../components/ChatPanel";

export default function DocumentChatPage({ params }: { params: { documentId: string } }) {
  return (
    <section className="section">
      <h1>Document chat</h1>
      <p className="muted">Answers are grounded in stored document chunks and returned with citations.</p>
      <ChatPanel documentId={params.documentId} />
    </section>
  );
}
