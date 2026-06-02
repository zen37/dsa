type Statement = {
  id: string;
  period_label?: string | null;
  currency?: string | null;
  rooms_revenue?: number | null;
  food_and_beverage_revenue?: number | null;
  other_revenue?: number | null;
  total_revenue?: number | null;
  gross_operating_profit?: number | null;
  ebitda?: number | null;
  net_operating_income?: number | null;
  metrics?: {
    occupancy?: number | null;
    adr?: number | null;
    revpar?: number | null;
    noi_per_key?: number | null;
    gop_margin?: number | null;
  } | null;
};

function money(value?: number | null) {
  if (value === null || value === undefined) return "";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value);
}

function number(value?: number | null) {
  if (value === null || value === undefined) return "";
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);
}

export default function FinancialsTable({ statements }: { statements: Statement[] }) {
  if (!statements.length) {
    return <p className="muted">No operating statements have been extracted yet.</p>;
  }

  return (
    <div className="panel">
      <h2>Financial summary</h2>
      <table>
        <thead>
          <tr>
            <th>Period</th>
            <th>Rooms revenue</th>
            <th>F&B revenue</th>
            <th>Total revenue</th>
            <th>GOP</th>
            <th>NOI</th>
            <th>Occ.</th>
            <th>ADR</th>
            <th>RevPAR</th>
          </tr>
        </thead>
        <tbody>
          {statements.map((statement) => (
            <tr key={statement.id}>
              <td>{statement.period_label || "Unknown"}</td>
              <td>{money(statement.rooms_revenue)}</td>
              <td>{money(statement.food_and_beverage_revenue)}</td>
              <td>{money(statement.total_revenue)}</td>
              <td>{money(statement.gross_operating_profit)}</td>
              <td>{money(statement.net_operating_income)}</td>
              <td>{number(statement.metrics?.occupancy)}</td>
              <td>{money(statement.metrics?.adr)}</td>
              <td>{money(statement.metrics?.revpar)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
