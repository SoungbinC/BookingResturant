from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from dependencies.auth import require_role
from dependencies.database import get_db
from models import UserRole, Restaurant, Reservation, BookingSlot
from schemas.restaurant_schema import RestaurantRead, RestaurantCreate, RestaurantUpdate
from schemas.reservation_schema import ReservationRead
from schemas.bookingslot_schema import BookingSlotCreate, BookingSlotRead
from services.restaurant_builder import RestaurantBuilder
from services.reservation_service import ReservationService

router = APIRouter(prefix="/manager", tags=["Manager API"])
get_manager = require_role(UserRole.MANAGER)

# -------------------------------
# 📌 Restaurant Management
# -------------------------------


@router.get("/my-restaurants", response_model=List[RestaurantRead])
def get_my_restaurants(
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    restaurants = db.query(Restaurant).filter(Restaurant.owner_id == user.id).all()
    return [RestaurantRead.from_orm(r) for r in restaurants]


# --------------------------------
# Create Restaurant
# ---------------------------------


@router.post("/restaurants", response_model=RestaurantRead)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    if restaurant_data.open_time >= restaurant_data.close_time:
        raise HTTPException(
            status_code=400, detail="Open time must be before close time."
        )

    builder = RestaurantBuilder(db=db, owner=user)
    builder.create_restaurant(restaurant_data)
    builder.add_booking_slots(restaurant_data.available_time_slots)
    restaurant = builder.build()

    return RestaurantRead.from_orm(restaurant)


# --------------------------------
# Update Restaurant
# ---------------------------------


@router.put("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id, Restaurant.owner_id == user.id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=404, detail="Restaurant not found or you're not the owner."
        )

    update_fields = restaurant_data.dict(exclude_unset=True)

    # Safety check: open < close
    if "open_time" in update_fields and "close_time" in update_fields:
        if update_fields["open_time"] >= update_fields["close_time"]:
            raise HTTPException(
                status_code=400, detail="Open time must be before close time."
            )

    for field, value in update_fields.items():
        setattr(restaurant, field, value)

    db.commit()
    db.refresh(restaurant)

    return RestaurantRead.from_orm(restaurant)


# ---------------------------------
# Add booking slots to restaurant
# ---------------------------------
@router.post(
    "/restaurants/{restaurant_id}/slots",
    response_model=List[BookingSlotRead],
    status_code=status.HTTP_201_CREATED,
)
def add_booking_slots_to_restaurant(
    restaurant_id: int,
    slots: List[BookingSlotCreate],
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == restaurant_id, Restaurant.owner_id == user.id)
        .first()
    )
    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found or you are not the owner.",
        )

    created_slots = []
    for slot_data in slots:
        if slot_data.start_time >= slot_data.end_time:
            raise HTTPException(
                status_code=400,
                detail="Slot start time must be before end time.",
            )
        slot = BookingSlot(
            restaurant_id=restaurant.id,
            start_time=slot_data.start_time,
            end_time=slot_data.end_time,
            table_size=slot_data.table_size,
            is_booked=False,
        )
        db.add(slot)
        created_slots.append(slot)

    db.commit()
    return [BookingSlotRead.from_orm(s) for s in created_slots]


# ---------------------------------
# Upload Restaurant Photos
# ---------------------------------


@router.post("/restaurants/{restaurant_id}/photos")
def upload_restaurant_photos(
    restaurant_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    # 🚧 TODO: Implement restaurant photo upload logic
    return {
        "message": f"Upload photos for restaurant {restaurant_id} - to be implemented"
    }


# ----------------------------------
# View Pending Restaurants
# -----------------------------------


@router.get("/my-pending-restaurants", response_model=List[RestaurantRead])
def get_pending_restaurants_manager(
    db: Session = Depends(get_db), user=Depends(get_manager)
):
    restaurants = (
        db.query(Restaurant)
        .filter(Restaurant.owner_id == user.id, Restaurant.is_approved == False)
        .all()
    )
    return [RestaurantRead.from_orm(r) for r in restaurants]


# -------------------------------
# 📆 Reservation Management
# -------------------------------


@router.get("/reservations", response_model=List[ReservationRead])
def get_all_reservations_for_manager(
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    reservations = (
        db.query(Reservation)
        .join(Restaurant)
        .filter(Restaurant.owner_id == user.id)
        .all()
    )
    return [ReservationRead.model_validate(r) for r in reservations]


@router.get(
    "/restaurants/{restaurant_id}/reservations", response_model=List[ReservationRead]
)
def get_reservations_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    reservations = (
        db.query(Reservation).filter(Reservation.restaurant_id == restaurant_id).all()
    )
    return [ReservationRead.model_validate(r) for r in reservations]


@router.post("/reservations/{reservation_id}/approve", response_model=ReservationRead)
def approve_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    service = ReservationService(db, user)
    reservation = service.approve_reservation(reservation_id)
    return ReservationRead.from_orm(reservation)


@router.post("/reservations/{reservation_id}/cancel", response_model=ReservationRead)
def cancel_reservation_as_manager(
    reservation_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_manager),
):
    service = ReservationService(db, user)
    reservation = service.cancel_by_manager(reservation_id)
    return ReservationRead.from_orm(reservation)
