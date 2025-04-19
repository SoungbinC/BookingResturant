from abc import ABC, abstractmethod
from models import Reservation
from fastapi import HTTPException


class ReservationState(ABC):
    @abstractmethod
    def confirm(self, reservation: Reservation):
        pass

    @abstractmethod
    def cancel(self, reservation: Reservation):
        pass


class PendingState(ReservationState):
    def confirm(self, reservation: Reservation):
        reservation.status = "CONFIRMED"
        reservation.booking_slot.book_slot()
        print(f"Reservation {reservation.id} confirmed.")

    def cancel(self, reservation: Reservation):
        reservation.status = "CANCELED"
        print(f"Reservation {reservation.id} canceled from pending.")


class ConfirmedState(ReservationState):
    def confirm(self, reservation: Reservation):
        raise HTTPException(400, "Reservation already confirmed.")

    def cancel(self, reservation: Reservation):
        reservation.status = "CANCELED"
        reservation.booking_slot.cancel_booking()
        print(f"Reservation {reservation.id} canceled from confirmed.")


class CanceledState(ReservationState):
    def confirm(self, reservation: Reservation):
        raise HTTPException(400, "Cannot confirm a canceled reservation.")

    def cancel(self, reservation: Reservation):
        raise HTTPException(400, "Reservation already canceled.")


class AvailableState(ReservationState):
    def confirm(self, reservation: Reservation):
        reservation.status = "PENDING"
        print(f"Reservation created and moved to PENDING.")

    def cancel(self, reservation: Reservation):
        raise HTTPException(400, "Cannot cancel: no reservation exists.")
