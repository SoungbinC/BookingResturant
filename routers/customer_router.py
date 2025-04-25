from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from typing import List

from dependencies.auth import require_role
from dependencies.database import get_db
from models import UserRole, Reservation, Review
from schemas.reservation_schema import (
    ReservationCreate,
    ReservationRead,
    ReservationCreateRequest,
    CancelReservationRequest,
)
from schemas.review_schema import ReviewCreate, ReviewRead
from services.reservation_service import ReservationService
from patterns.command import BookTableCommand, CancelReservationCommand
from services.notification_service import notify

router = APIRouter(prefix="/customers", tags=["Customer API"])
get_customer = require_role(UserRole.CUSTOMER)


# -------------------
# Profile Routes
# -------------------
@router.get("/profile")
def get_profile(user=Depends(get_customer)):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
    }


# -------------------
# Reservation Routes
# -------------------
@router.get("/reservations/me", response_model=List[ReservationRead])
def get_my_reservations(db: Session = Depends(get_db), user=Depends(get_customer)):
    reservations = db.query(Reservation).filter(Reservation.user_id == user.id).all()
    return [ReservationRead.from_orm(r) for r in reservations]


@router.post("/reservations", response_model=ReservationRead)
def create_reservation(
    request_data: ReservationCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_customer),
):
    reservation_data = ReservationCreate(
        **request_data.dict(),
        user_id=user.id,
        status="pending",
    )

    reservation_service = ReservationService(db, user)
    command = BookTableCommand(reservation_service, reservation_data)
    reservation = command.execute()

    notify(reservation, "reservation_pending")
    return ReservationRead.from_orm(reservation)


@router.post("/reservations/cancel", response_model=ReservationRead)
def cancel_reservation_and_release_slot(
    payload: CancelReservationRequest,
    db: Session = Depends(get_db),
    user=Depends(get_customer),
):
    reservation_service = ReservationService(db, user)

    command = CancelReservationCommand(
        reservation_service,
        restaurant_id=payload.restaurant_id,
        booking_slot_id=payload.booking_slot_id,
        user_id=user.id,
    )

    # notify(reservation, "reservation_canceled")  # ✅ updated
    reservation = command.execute()

    return ReservationRead.from_orm(reservation)


# -------------------
# Review Routes
# -------------------
@router.post("/restaurants/{restaurant_id}/reviews", response_model=ReviewRead)
def create_review_for_restaurant(
    restaurant_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(get_customer),
):
    review = Review(
        user_id=user.id,
        restaurant_id=restaurant_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
