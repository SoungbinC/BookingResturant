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
from sqlalchemy.orm import relationship
from .common import Base
from .user import User
import enum


class RestaurantStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    RENOVATING = "renovating"


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)

    address = Column(String)
    map_url = Column(String)

    city = Column(String)
    state = Column(String)
    zipcode = Column(String)

    cuisine = Column(String)
    price_range = Column(String)
    rating = Column(Float)

    open_mon = Column(String)
    open_tue = Column(String)
    open_wed = Column(String)
    open_thu = Column(String)
    open_fri = Column(String)
    open_sat = Column(String)
    open_sun = Column(String)

    photo_url = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    status = Column(
        Enum(RestaurantStatus, name="restaurant_status_enum", create_type=False),
        default=RestaurantStatus.OPEN,
    )

    is_approved = Column(Boolean, default=False)

    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    owner = relationship("User", back_populates="restaurants")

    booking_slots = relationship("BookingSlot", back_populates="restaurant")
    reservations = relationship("Reservation", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
