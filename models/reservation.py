# modules/reservation.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .common import Base
from .user import User
from .restaurant import Restaurant
import enum
from sqlalchemy import Enum


class ReservationStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    booking_slot_id = Column(
        Integer,
        ForeignKey(
            "booking_slots.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    reservation_time = Column(DateTime, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    status = Column(
        Enum(ReservationStatus, name="reservation_status_enum"),
        default=ReservationStatus.PENDING,
    )

    # Relationships
    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")
    booking_slot = relationship("BookingSlot", back_populates="reservations")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def book_slot(self):
        if not self.booking_slot.is_booked:
            self.booking_slot.book_slot()  # Mark the slot as booked
        else:
            raise Exception("Slot is already booked.")

    def cancel_slot(self):
        if self.booking_slot.is_booked:
            self.booking_slot.cancel_booking()  # Cancel the booking
        else:
            raise Exception("Slot is already available.")
