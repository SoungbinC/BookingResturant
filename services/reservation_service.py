from models import Reservation, BookingSlot
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.state_resolver import get_state_instance
from patterns.chain.handlers import (
    CustomerCancelHandler,
    ManagerAccessHandler,
    AdminAccessHandler,
)
from patterns.chain.base_handler import BaseAccessHandler


class ReservationService:
    def __init__(self, db: Session, current_user):
        self.db = db
        self.current_user = current_user

    def book(self, reservation_data):
        """Customer requests a reservation (initially PENDING)"""
        user_id = self.current_user.id

        slot = (
            self.db.query(BookingSlot)
            .filter(BookingSlot.id == reservation_data.booking_slot_id)
            .first()
        )

        if not slot:
            raise HTTPException(status_code=404, detail="Booking slot not found.")
        if slot.restaurant_id != reservation_data.restaurant_id:
            raise HTTPException(
                status_code=400, detail="Slot doesn't match restaurant."
            )
        if slot.is_booked:
            raise HTTPException(status_code=400, detail="Slot already booked.")

        reservation = Reservation(
            user_id=user_id,
            restaurant_id=reservation_data.restaurant_id,
            booking_slot_id=reservation_data.booking_slot_id,
            reservation_time=reservation_data.reservation_time,
            number_of_people=reservation_data.number_of_people,
            status="PENDING",
        )

        slot.is_booked = True

        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def cancel(self, restaurant_id: int, booking_slot_id: int, user_id: int):
        reservation = (
            self.db.query(Reservation)
            .filter(
                Reservation.restaurant_id == restaurant_id,
                Reservation.user_id == user_id,
                Reservation.booking_slot_id == booking_slot_id,
            )
            .first()
        )

        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found.")

        # ✅ Chain of Responsibility for cancellation
        access_chain = CustomerCancelHandler(ManagerAccessHandler(AdminAccessHandler()))
        access_chain.handle(self.current_user, reservation)

        state = get_state_instance(reservation)
        state.cancel(reservation)

        slot = (
            self.db.query(BookingSlot)
            .filter(BookingSlot.id == reservation.booking_slot_id)
            .first()
        )

        if slot:
            slot.is_booked = False

        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def approve_reservation(self, reservation_id: int):
        reservation = (
            self.db.query(Reservation)
            .join(Reservation.restaurant)
            .filter(Reservation.id == reservation_id)
            .first()
        )

        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found.")
        if reservation.status != "PENDING":
            raise HTTPException(status_code=400, detail="Reservation must be pending.")

        # ✅ Chain of Responsibility for approval
        access_chain = ManagerAccessHandler(AdminAccessHandler())
        access_chain.handle(self.current_user, reservation)

        state = get_state_instance(reservation)
        state.confirm(reservation)

        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def cancel_by_manager(self, reservation_id: int):
        reservation = (
            self.db.query(Reservation)
            .join(Reservation.restaurant)
            .filter(Reservation.id == reservation_id)
            .first()
        )

        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found.")

        # ✅ Chain of Responsibility (manager/admin)
        access_chain = ManagerAccessHandler(AdminAccessHandler())
        access_chain.handle(self.current_user, reservation)

        state = get_state_instance(reservation)
        state.cancel(reservation)

        self.db.commit()
        self.db.refresh(reservation)
        return reservation
