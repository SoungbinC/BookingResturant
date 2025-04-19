# patterns/chain/handlers.py

from .base_handler import BaseAccessHandler  # ✅ works within the same package
from models import UserRole


class CustomerCancelHandler(BaseAccessHandler):
    def can_handle(self, user, reservation):
        return user.role == UserRole.CUSTOMER and reservation.user_id == user.id


class ManagerAccessHandler(BaseAccessHandler):
    def can_handle(self, user, reservation):
        return (
            user.role == UserRole.MANAGER
            and reservation.restaurant
            and reservation.restaurant.owner_id == user.id
        )


class AdminAccessHandler(BaseAccessHandler):
    def can_handle(self, user, reservation):
        return user.role == UserRole.ADMIN
