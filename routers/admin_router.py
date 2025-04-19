from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from dependencies.auth import require_role
from dependencies.database import get_db
from models import UserRole, Reservation, Restaurant, Review
from schemas.reservation_schema import ReservationRead
from schemas.restaurant_schema import RestaurantRead
from services.notification_service import notify

router = APIRouter(prefix="/admin", tags=["Admin API"])


# -------------------
# Admin: View All Reservations
# -------------------
@router.get("/reservations", response_model=List[ReservationRead])
def get_all_reservations(
    db: Session = Depends(get_db), user=Depends(require_role(UserRole.ADMIN))
):
    reservations = db.query(Reservation).all()
    return [ReservationRead.from_orm(r) for r in reservations]


# -------------------
# Admin: View pending Restaurants
# -------------------
@router.get("/pending-restaurants", response_model=List[RestaurantRead])
def get_pending_restaurants_admin(
    db: Session = Depends(get_db), user=Depends(require_role(UserRole.ADMIN))
):
    restaurants = db.query(Restaurant).filter(Restaurant.is_approved == False).all()
    return [RestaurantRead.from_orm(r) for r in restaurants]


# -------------------
# Admin: Approve Restaurant
# -------------------
@router.post("/approve-restaurant/{restaurant_id}")
def approve_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if restaurant.is_approved:
        return {"message": "Restaurant is already approved"}

    restaurant.is_approved = True
    db.commit()

    notify(restaurant, "restaurant_approved")

    return {"message": f"Restaurant {restaurant.name} approved successfully"}


# -------------------
# Admin: Delete Restaurant
# -------------------
@router.delete("/restaurants/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db.delete(restaurant)
    db.commit()
    return {"message": f"Restaurant {restaurant.name} deleted successfully"}


# -------------------
# Admin: Analytics Dashboard (Placeholder)
# -------------------
@router.get("/analytics")
def get_admin_analytics(
    db: Session = Depends(get_db), user=Depends(require_role(UserRole.ADMIN))
):
    # Example dummy analytics data
    total_reservations = db.query(Reservation).count()
    total_restaurants = db.query(Restaurant).count()

    return {
        "total_reservations": total_reservations,
        "total_restaurants": total_restaurants,
    }


# -------------------
# Admin: Moderate Review
# -------------------
@router.post("/moderate-review/{review_id}")
def moderate_review(
    review_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(UserRole.ADMIN)),
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Example action: mark as moderated or delete
    db.delete(review)
    db.commit()
    return {"message": f"Review {review_id} has been removed by admin"}
