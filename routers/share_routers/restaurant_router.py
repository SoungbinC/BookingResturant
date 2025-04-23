from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from dependencies.auth import get_current_user, require_role
from dependencies.database import get_db
from models import Restaurant, BookingSlot, Review, UserRole
from schemas.restaurant_schema import RestaurantRead
from schemas.bookingslot_schema import BookingSlotRead
from schemas.review_schema import ReviewCreate, ReviewRead

from patterns.strategy import SearchStrategy
from services.search_service import (
    NameSearchStrategy,
    CitySearchStrategy,
    CuisineSearchStrategy,
    ZipSearchStrategy,
    TimeWindowSlotStrategy,
    SearchContext,
)
from services.slot_service import get_available_slots_for_restaurant

router = APIRouter(prefix="/restaurants", tags=["Shared/ Restaurants API"])


# -----------------------------------------------
# 📋 Show All Restaurants
# -----------------------------------------------
@router.get("/", response_model=List[RestaurantRead])
def get_all_restaurants(db: Session = Depends(get_db)):
    try:
        # Retrieve all restaurants from the database
        restaurants = db.query(Restaurant).all()

        if not restaurants:
            raise HTTPException(status_code=404, detail="No restaurants found")

        # Return a list of restaurants serialized using the RestaurantRead schema
        return [RestaurantRead.from_orm(restaurant) for restaurant in restaurants]

    except Exception as e:
        # Log error for debugging
        print("Error retrieving all restaurants:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurants")


# -----------------------------------------------
# 📋 Get Restaurant by ID
# -----------------------------------------------
@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the restaurant by ID from the database
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

        # If no restaurant is found, raise a 404 error
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Return the restaurant serialized using the RestaurantRead schema
        return RestaurantRead.from_orm(restaurant)

    except Exception as e:
        print("Error retrieving restaurant by ID:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch restaurant")


# -----------------------------------------------
# 🔍 Restaurant Search with Availability
# -----------------------------------------------
@router.get("/search", response_model=List[RestaurantRead])
def search_restaurants(
    name: Optional[str] = None,
    city: Optional[str] = None,
    cuisine: Optional[str] = None,
    zipcode: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Restaurant)

        strategies: List[Tuple[SearchStrategy, Optional[str]]] = [
            (NameSearchStrategy(), name),
            (CitySearchStrategy(), city),
            (CuisineSearchStrategy(), cuisine),
            (ZipSearchStrategy(), zipcode),
        ]

        if date and time:
            search_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            time_window = (
                search_datetime - timedelta(minutes=30),
                search_datetime + timedelta(minutes=30),
            )
            strategies.append((TimeWindowSlotStrategy(), time_window))

        filtered_query = SearchContext(strategies).apply_filters(query)
        restaurants = filtered_query.limit(10).all()
        return [RestaurantRead.from_orm(r) for r in restaurants]

    except Exception as e:
        print("Search failed:", e)
        raise HTTPException(status_code=500, detail="Restaurant search failed")


# -----------------------------------------------
# ⭐ Review Endpoints (Customer)
# -----------------------------------------------
@router.post("/{restaurant_id}/reviews", response_model=ReviewRead)
def create_review_for_restaurant(
    restaurant_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(UserRole.CUSTOMER)),
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


@router.get("/{restaurant_id}/reviews", response_model=List[ReviewRead])
def get_reviews_for_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    return db.query(Review).filter(Review.restaurant_id == restaurant_id).all()


# -----------------------------------------------
# 📆 Get Available Booking Slots
# -----------------------------------------------
@router.get("/{restaurant_id}/available-slots", response_model=List[BookingSlotRead])
def get_available_slots(
    restaurant_id: int,
    db: Session = Depends(get_db),
):
    slots = get_available_slots_for_restaurant(db, restaurant_id)
    return [BookingSlotRead.from_orm(slot) for slot in slots]
