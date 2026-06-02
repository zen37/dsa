export default function DocumentStatus({ status }: { status?: string | null }) {
  const normalized = status || "uploaded";
  return <span className={`status ${normalized}`}>{normalized}</span>;
}
