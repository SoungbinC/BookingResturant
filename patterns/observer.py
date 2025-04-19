from abc import ABC, abstractmethod


# -----------------------------
# Observer Base + Implementations
# -----------------------------
class Observer(ABC):
    @abstractmethod
    def update(self, entity, event: str):
        pass


class EmailNotifier(Observer):
    def update(self, entity, event: str):
        if event == "reservation_pending":
            print(
                f"[EMAIL] 🕒 Reservation is pending for user {entity.user_id} at restaurant {entity.restaurant_id}."
            )
        elif event == "reservation_approved":
            print(
                f"[EMAIL] ✅ Reservation for user {entity.user_id} at restaurant {entity.restaurant_id} approved."
            )
        elif event == "reservation_canceled":
            print(
                f"[EMAIL] ❌ Reservation for user {entity.user_id} at restaurant {entity.restaurant_id} has been canceled."
            )
        elif event == "restaurant_pending":
            print(
                f"[EMAIL] 🕒 Restaurant '{entity.name}' (ID: {entity.id}) is awaiting admin approval."
            )
        elif event == "restaurant_approved":
            print(
                f"[EMAIL] ✅ Restaurant '{entity.name}' (ID: {entity.id}) has been approved!"
            )


class SMSNotifier(Observer):
    def update(self, entity, event: str):
        if event == "reservation_pending":
            print(
                f"[SMS] 🕒 Pending reservation for user {entity.user_id} at restaurant {entity.restaurant_id}."
            )
        elif event == "reservation_approved":
            print(
                f"[SMS] ✅ Reservation for user {entity.user_id} at restaurant {entity.restaurant_id} approved."
            )
        elif event == "reservation_canceled":
            print(
                f"[SMS] ❌ Reservation for user {entity.user_id} at restaurant {entity.restaurant_id} canceled."
            )
        elif event == "restaurant_pending":
            print(
                f"[SMS] 🕒 Restaurant '{entity.name}' (ID: {entity.id}) is pending approval."
            )
        elif event == "restaurant_approved":
            print(f"[SMS] ✅ Restaurant '{entity.name}' (ID: {entity.id}) approved!")


# -----------------------------
# Notification System
# -----------------------------
class ReservationNotifier:
    def __init__(self):
        self._observers = []

    def register(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, entity, event: str):
        for observer in self._observers:
            observer.update(entity, event)


# -----------------------------
# Centralized NotificationService
# -----------------------------
class NotificationService:
    _instance = None  # Singleton instance

    def __init__(self):
        self.notifier = ReservationNotifier()
        self.notifier.register(EmailNotifier())
        self.notifier.register(SMSNotifier())

    def send(self, entity, event: str):
        self.notifier.notify(entity, event)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = NotificationService()
        return cls._instance
