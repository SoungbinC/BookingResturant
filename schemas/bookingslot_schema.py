from pydantic import BaseModel
from datetime import datetime


# Schema for creating a booking slot
class BookingSlotCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    table_size: int
    is_booked: bool = False
    table_size: int = 0

    class Config:
        from_attributes = True


# Schema for reading a booking slot
class BookingSlotRead(BaseModel):
    id: int
    restaurant_id: int
    start_time: str
    end_time: str
    is_booked: bool
    table_size: int

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            restaurant_id=obj.restaurant_id,
            start_time=obj.start_time.isoformat(),  # Convert datetime to ISO string
            end_time=obj.end_time.isoformat(),
            is_booked=obj.is_booked,
            table_size=obj.table_size,
        )


# Schema for updating a booking slot
class BookingSlotUpdate(BaseModel):
    status: str  # Update slot status (e.g., "AVAILABLE", "BOOKED")

    class Config:
        from_attributes = True
