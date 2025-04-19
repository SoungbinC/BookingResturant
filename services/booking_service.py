# services/booking_service.py
from models.reservation import Reservation
from dependencies.database import Database
from patterns.state import RequestedState, ConfirmedState, CanceledState


class BookingService:
    def __init__(self):
        self.db = Database.get_instance().Session()

    def book(self, reservation_data):
        reservation = Reservation(**reservation_data.dict())
        reservation.change_state(RequestedState())
        self.db.add(reservation)
        self.db.commit()
        reservation.change_state(ConfirmedState())
        self.db.commit()
        return reservation

    def cancel(self, reservation_id):
        reservation = self.db.query(Reservation).get(reservation_id)
        reservation.change_state(CanceledState())
        self.db.commit()
        return reservation
