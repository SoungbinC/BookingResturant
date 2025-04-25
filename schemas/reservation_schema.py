from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from schemas.bookingslot_schema import BookingSlotRead


class ReservationCreateRequest(BaseModel):
    restaurant_id: int
    reservation_time: datetime
    number_of_people: int
    booking_slot_id: int


# Schema for creating a reservation
class ReservationCreate(BaseModel):
    restaurant_id: int
    user_id: int
    reservation_time: datetime
    number_of_people: int
    status: Optional[str] = "pending"  # Default status is "pending"
    booking_slot_id: int  # Use a single booking slot ID

    class Config:
        from_attributes = True


# Schema for reading a reservation
class ReservationRead(BaseModel):
    id: int
    restaurant_id: int
    user_id: int
    reservation_time: datetime
    number_of_people: int
    status: str
    booking_slot: BookingSlotRead  # Nested object

    model_config = ConfigDict(from_attributes=True)  # Enables ORM conversion

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            restaurant_id=obj.restaurant_id,
            user_id=obj.user_id,
            reservation_time=obj.reservation_time.isoformat(),  # Convert datetime to ISO string
            number_of_people=obj.number_of_people,
            status=obj.status.value,  # Enum to value
            booking_slot=BookingSlotRead.from_orm(
                obj.booking_slot
            ),  # Convert the single booking_slot to BookingSlotRead
        )
