from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime, time
from schemas.bookingslot_schema import BookingSlotCreate
from enum import Enum
from models import RestaurantStatus
from datetime import time


# Enum for Restaurant Status
class RestaurantStatusEnum(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    RENOVATING = "RENOVATING"


# Create Model for Restaurants
class RestaurantCreate(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zipcode: str
    cuisine: str
    price_range: str  # Updated to price_range
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


# DB model for restaurant with owner_id and approval flag
class RestaurantDB(RestaurantCreate):
    owner_id: int
    is_approved: Optional[bool] = False


# Model for Restaurant Read Response
class RestaurantRead(BaseModel):
    id: int
    name: str
    description: str
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    cuisine: Optional[str] = None
    price_range: Optional[str] = None
    rating: Optional[float] = None
    open_mon: Optional[str] = None
    open_tue: Optional[str] = None
    open_wed: Optional[str] = None
    open_thu: Optional[str] = None
    open_fri: Optional[str] = None
    open_sat: Optional[str] = None
    open_sun: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: str
    updated_at: str
    status: RestaurantStatusEnum
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
        obj.status = obj.status.name if obj.status else RestaurantStatusEnum.OPEN.value
        obj.is_approved = obj.is_approved if obj.is_approved is not None else False
        return super().from_orm(obj)


# Model for searching restaurants
class RestaurantSearch(BaseModel):
    cuisine: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    available_time_slots: Optional[List[str]] = None

    class Config:
        from_attributes = True


# Model for updating a restaurant's information
class RestaurantUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    cuisine: Optional[str]
    price_range: Optional[str]  # Changed from cost_rating to price_range
    open_time: Optional[time]
    close_time: Optional[time]
    description: Optional[str]
    photo_url: Optional[str]

    class Config:
        from_attributes = True


# Model for updating restaurant status
class RestaurantStatusUpdate(BaseModel):
    status: RestaurantStatusEnum

    class Config:
        from_attributes = True


# Restaurant Model in the database
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Boolean,
    Float,
    Text,
    Time,
)
