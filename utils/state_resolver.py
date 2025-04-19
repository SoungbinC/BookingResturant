from models import Reservation
from patterns.state import PendingState, ConfirmedState, CanceledState


def get_state_instance(reservation: Reservation):
    if reservation.status == "PENDING":
        return PendingState()
    elif reservation.status == "CONFIRMED":
        return ConfirmedState()
    elif reservation.status == "CANCELED":
        return CanceledState()
    else:
        raise ValueError(f"Unknown reservation state: {reservation.status}")
