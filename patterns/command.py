class Command:
    def execute(self):
        raise NotImplementedError()


class BookTableCommand(Command):
    def __init__(self, reservation_service, reservation_data):
        self.reservation_service = reservation_service
        self.reservation_data = reservation_data

    def execute(self):
        return self.reservation_service.book(self.reservation_data)


class CancelReservationCommand(Command):
    def __init__(self, reservation_service, reservation_id, booking_slot_id, user_id):
        self.reservation_service = reservation_service
        self.reservation_id = reservation_id
        self.booking_slot_id = booking_slot_id
        self.user_id = user_id

    def execute(self):
        return self.reservation_service.cancel(
            self.reservation_id, self.booking_slot_id, self.user_id
        )
