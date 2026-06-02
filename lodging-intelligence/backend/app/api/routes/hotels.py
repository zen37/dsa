from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.services.hotel_service import HotelService

router = APIRouter(prefix="/api/hotels", tags=["hotels"])


@router.get("")
def list_hotels():
    return HotelService().list_hotels()


@router.get("/{hotel_id}")
def get_hotel(hotel_id: str):
    detail = HotelService().get_hotel_detail(hotel_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")
    return detail
