# modules/bookingslot.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .common import Base


class BookingSlot(Base):
    __tablename__ = "booking_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(
        Integer,
        ForeignKey(
            "restaurants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)

    table_size = Column(Integer, nullable=False)  # Required to match # of people

    restaurant = relationship("Restaurant", back_populates="booking_slots")
    reservations = relationship("Reservation", back_populates="booking_slot")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def book_slot(self):
        if not self.is_booked:
            self.is_booked = True
        else:
            raise Exception("Slot is already booked.")

    def cancel_booking(self):
        if self.is_booked:
            self.is_booked = False
        else:
            raise Exception("Slot is already available.")
