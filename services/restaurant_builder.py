from models import Restaurant, BookingSlot
from schemas.restaurant_schema import RestaurantCreate
from schemas.bookingslot_schema import BookingSlotCreate
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List


class RestaurantBuilder:
    def __init__(self, db: Session, owner):
        self.db = db
        self.owner = owner
        self.restaurant = None

    def create_restaurant(self, data: RestaurantCreate):
        self.restaurant = Restaurant(
            name=data.name,
            address=data.address,
            city=data.city,
            state=data.state,
            zipcode=data.zipcode,
            cuisine=data.cuisine,
            cost_rating=data.cost_rating,
            open_time=data.open_time,
            close_time=data.close_time,
            description=data.description,
            photo_url=data.photo_url,
            status="OPEN",
            owner_id=self.owner.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_approved=False,
        )
        self.db.add(self.restaurant)

    def add_booking_slots(self, slots: Optional[List[BookingSlotCreate]]):
        if not slots:
            return  # ✅ Safe exit if no slots passed
        for slot_data in slots:
            slot = BookingSlot(
                restaurant=self.restaurant,
                start_time=slot_data.start_time,
                end_time=slot_data.end_time,
                table_size=slot_data.table_size,
                is_booked=False,
            )
            self.db.add(slot)

    def build(self):
        self.db.commit()
        self.db.refresh(self.restaurant)
        return self.restaurant
