# models/restaurant.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    ARRAY,
    Boolean,
)
from sqlalchemy.orm import relationship
from .common import Base
from .user import User  # Import User model for relationship
import enum
from sqlalchemy import Time


class RestaurantStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    RENOVATING = "renovating"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    cuisine = Column(String)
    cost_rating = Column(Integer)

    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)

    description = Column(String)
    photo_url = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    status = Column(
        Enum(RestaurantStatus, name="restaurant_status_enum", create_type=False),
        default=RestaurantStatus.OPEN,
    )

    is_approved = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="restaurants")

    booking_slots = relationship("BookingSlot", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
