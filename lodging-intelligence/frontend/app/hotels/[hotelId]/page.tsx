import FinancialsTable from "../../../components/FinancialsTable";
import HotelProfileCard from "../../../components/HotelProfileCard";

const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function getHotel(hotelId: string) {
  const response = await fetch(`${apiBase}/api/hotels/${hotelId}`, { cache: "no-store" });
  if (!response.ok) return null;
  return response.json();
}

export default async function HotelDetailPage({ params }: { params: { hotelId: string } }) {
  const detail = await getHotel(params.hotelId);

  if (!detail) {
    return <p className="muted">Hotel not found.</p>;
  }

  return (
    <section className="section">
      <div className="button-row" style={{ justifyContent: "space-between" }}>
        <h1>{detail.hotel.name || "Hotel detail"}</h1>
        <div className="button-row">
          <a className="button secondary" href={`${apiBase}/api/hotels/${params.hotelId}/export/json`}>
            Export JSON
          </a>
          <a className="button secondary" href={`${apiBase}/api/hotels/${params.hotelId}/export/csv`}>
            Export CSV
          </a>
        </div>
      </div>
      <HotelProfileCard hotel={detail.hotel} />
      <div style={{ height: 18 }} />
      <FinancialsTable statements={detail.operatingStatements || []} />
    </section>
  );
}
