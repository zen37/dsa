from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status

from app.services.export_service import ExportService

router = APIRouter(prefix="/api/hotels", tags=["exports"])


@router.get("/{hotel_id}/export/json")
def export_hotel_json(hotel_id: str):
    payload = ExportService().export_json(hotel_id)
    if not payload:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return payload


@router.get("/{hotel_id}/export/csv")
def export_hotel_csv(hotel_id: str):
    payload = ExportService().export_csv(hotel_id)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return Response(
        content=payload,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="hotel-{hotel_id}.csv"'},
    )
