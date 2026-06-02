type Hotel = {
  name?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  country?: string | null;
  market?: string | null;
  key_count?: number | null;
  brand?: string | null;
  management_company?: string | null;
};

function Field({ label, value }: { label: string; value?: string | number | null }) {
  return (
    <div>
      <span className="label">{label}</span>
      <span className="value">{value || "Not extracted"}</span>
    </div>
  );
}

export default function HotelProfileCard({ hotel }: { hotel: Hotel }) {
  return (
    <section className="panel">
      <h2>{hotel.name || "Hotel profile"}</h2>
      <div className="field-grid">
        <Field label="Address" value={hotel.address} />
        <Field label="City" value={hotel.city} />
        <Field label="State" value={hotel.state} />
        <Field label="Country" value={hotel.country} />
        <Field label="Market" value={hotel.market} />
        <Field label="Keys" value={hotel.key_count} />
        <Field label="Brand" value={hotel.brand} />
        <Field label="Management" value={hotel.management_company} />
      </div>
    </section>
  );
}
