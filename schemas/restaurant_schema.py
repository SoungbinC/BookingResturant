from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from schemas.bookingslot_schema import BookingSlotCreate
from enum import Enum
from models import RestaurantStatus
from datetime import time


class RestaurantStatusEnum(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RENOVATING = "RENOVATING"


class RestaurantCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zipcode: str
    cuisine: str
    cost_rating: int
    open_time: time
    close_time: time
    description: Optional[str] = None
    photo_url: Optional[str] = None
    available_time_slots: List[BookingSlotCreate] = None

    @validator("close_time")
    def validate_time(cls, close_time, values):
        open_time = values.get("open_time")
        if open_time and close_time <= open_time:
            raise ValueError("close_time must be after open_time.")
        return close_time

    class Config:
        from_attributes = True


class RestaurantDB(RestaurantCreate):
    owner_id: int
    is_approved: Optional[bool] = False


class RestaurantRead(BaseModel):
    id: int
    name: str
    address: str
    city: str
    state: str
    zipcode: str
    cuisine: str
    cost_rating: int
    created_at: str
    updated_at: str
    available_time_slots: List[str]
    status: RestaurantStatus
    is_approved: bool

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        obj.created_at = obj.created_at.isoformat() if obj.created_at else None
        obj.updated_at = obj.updated_at.isoformat() if obj.updated_at else None
        obj.available_time_slots = (
            [
                f"{slot.start_time.isoformat()} - {slot.end_time.isoformat()}"
                for slot in obj.booking_slots
            ]
            if obj.booking_slots
            else []
        )
        obj.status = obj.status if obj.status else RestaurantStatus.OPEN
        obj.is_approved = obj.is_approved if obj.is_approved is not None else False
        return super().from_orm(obj)


class RestaurantSearch(BaseModel):
    cuisine: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    available_time_slots: Optional[List[str]] = (
        None  # Could be used for filtering based on available slots
    )

    class Config:
        from_attributes = True


class RestaurantUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    cuisine: Optional[str]
    cost_rating: Optional[int]
    open_time: Optional[time]
    close_time: Optional[time]
    description: Optional[str]
    photo_url: Optional[str]

    class Config:
        from_attributes = True


class RestaurantStatusUpdate(BaseModel):
    status: RestaurantStatusEnum

    class Config:
        from_attributes = True
