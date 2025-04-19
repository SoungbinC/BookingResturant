from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import UserRole, User, Restaurant, Reservation
from dependencies.database import get_db
from patterns.chain.base_handler import BaseAccessHandler


class CustomerAccessHandler(BaseAccessHandler):
    def can_handle(self, user, reservation=None):
        # Check if the user is a Customer
        return user.role == UserRole.CUSTOMER

    def handle(self, user, db: Session):
        # Customer: return the user's reservation details only
        reservations = (
            db.query(Reservation).filter(Reservation.user_id == user.id).all()
        )
        if not reservations:
            raise HTTPException(status_code=404, detail="No reservations found.")
        return {"user_profile": user, "reservations": reservations}


class ManagerAccessHandler(BaseAccessHandler):
    def can_handle(self, user, reservation=None):
        # Check if the user is a Manager
        return user.role == UserRole.MANAGER

    def handle(self, user, db: Session):
        # Manager: return the restaurants they own and the reservations
        restaurants = db.query(Restaurant).filter(Restaurant.owner_id == user.id).all()
        if not restaurants:
            raise HTTPException(status_code=404, detail="No restaurants found.")

        restaurant_data = []
        for restaurant in restaurants:
            reservations = (
                db.query(Reservation)
                .filter(Reservation.restaurant_id == restaurant.id)
                .all()
            )
            restaurant_data.append(
                {"restaurant": restaurant, "reservations": reservations}
            )

        return {"user_profile": user, "owned_restaurants": restaurant_data}


class AdminAccessHandler(BaseAccessHandler):
    def can_handle(self, user, reservation=None):
        # Check if the user is an Admin
        return user.role == UserRole.ADMIN

    def handle(self, user, db: Session):
        # Admin: return the number of restaurants and reservations
        restaurant_count = db.query(Restaurant).count()
        reservation_count = db.query(Reservation).count()
        return {
            "user_profile": user,
            "restaurant_count": restaurant_count,
            "reservation_count": reservation_count,
        }
