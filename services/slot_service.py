# services/slot_service.py

from models import BookingSlot
from sqlalchemy.orm import Session
from typing import List


def get_available_slots_for_restaurant(
    db: Session, restaurant_id: int
) -> List[BookingSlot]:
    return (
        db.query(BookingSlot)
        .filter(
            BookingSlot.restaurant_id == restaurant_id, BookingSlot.is_booked == False
        )
        .all()
    )
