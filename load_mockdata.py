from models import (
    User,
    Restaurant,
    BookingSlot,
    Reservation,
    RestaurantStatus,
    UserRole,
    Review,
)
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from faker import Faker
import random
from passlib.context import CryptContext
from datetime import time

fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_users(db: Session):
    users = []

    # Explicit roles: 3 customers, 1 manager, 1 admin
    fixed_roles = [
        UserRole.CUSTOMER,
        UserRole.CUSTOMER,
        UserRole.CUSTOMER,
        UserRole.MANAGER,
        UserRole.ADMIN,
    ]

    print("Mock Users Created:")
    for i, role in enumerate(fixed_roles):
        raw_password = f"testpass{i}"
        hashed_pw = pwd_context.hash(raw_password)
        user = User(
            username=fake.user_name(),
            email=f"testuser{i}@example.com",
            hashed_password=hashed_pw,
            role=role,
        )
        db.add(user)
        users.append(user)
        print(f"Email: {user.email}, Password: {raw_password}, Role: {user.role.value}")

    db.commit()
    return users


def create_restaurants(db: Session, users):
    restaurants = []
    all_slots = []

    for _ in range(5):
        owner_candidates = [u for u in users if u.role == UserRole.MANAGER]
        if not owner_candidates:
            continue

        owner = random.choice(owner_candidates)
        status = random.choice(
            [
                RestaurantStatus.OPEN,
                RestaurantStatus.CLOSED,
                RestaurantStatus.RENOVATING,
            ]
        )

        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            state=fake.state(),
            zipcode=fake.zipcode(),
            cuisine=fake.word(),
            cost_rating=random.randint(1, 5),
            open_time=time(hour=10, minute=0),  # opens at 10:00 AM
            close_time=time(hour=22, minute=0),  # closes at 10:00 PM
            description=fake.sentence(nb_words=10),
            photo_url=fake.image_url(),
            created_at=fake.date_this_decade(),
            updated_at=fake.date_this_decade(),
            status=status,
            is_approved=False,  # still pending
            owner_id=owner.id,
        )
        db.add(restaurant)
        db.commit()

        slots = []
        for _ in range(3):
            slot = BookingSlot(
                restaurant_id=restaurant.id,
                start_time=datetime.now() + timedelta(days=random.randint(1, 10)),
                end_time=datetime.now()
                + timedelta(days=random.randint(1, 10), hours=2),
                table_size=random.choice([2, 4, 6]),
                is_booked=False,
            )
            db.add(slot)
            slots.append(slot)
            all_slots.append(slot)

        restaurants.append((restaurant, slots))

    db.commit()
    return restaurants, all_slots


def create_reservations(db: Session, restaurants_with_slots, users):
    print("\nMock Reservations Created:")
    used_slots = set()
    customer_users = [u for u in users if u.role == UserRole.CUSTOMER]

    for restaurant, slots in restaurants_with_slots:
        if not customer_users:
            break
        for slot in slots[:1]:  # Limit to 1 reservation per slot
            if slot.id in used_slots:
                continue
            user = random.choice(customer_users)

            reservation = Reservation(
                restaurant_id=restaurant.id,
                user_id=user.id,
                booking_slot_id=slot.id,
                reservation_time=slot.start_time,
                number_of_people=random.randint(1, 6),
                status="PENDING",
            )
            slot.is_booked = True  # ✅ mark booked
            db.add(reservation)
            used_slots.add(slot.id)
            print(
                f"User: {user.email}, Restaurant: {restaurant.name}, Slot: {slot.start_time}"
            )

    db.commit()


def create_reviews(db: Session, users, restaurants):
    print("\nMock Reviews Created:")
    customer_users = [u for u in users if u.role == UserRole.CUSTOMER]
    for restaurant, _ in restaurants:
        for _ in range(random.randint(1, 3)):  # 1-3 reviews per restaurant
            user = random.choice(customer_users)
            review = Review(
                user_id=user.id,
                restaurant_id=restaurant.id,
                rating=random.randint(1, 5),
                comment=fake.sentence(nb_words=12),
            )
            db.add(review)
            print(
                f"User: {user.email} reviewed Restaurant: {restaurant.name} - Rating: {review.rating}"
            )

    db.commit()


def load_mock_data(db: Session):
    users = create_users(db)
    restaurants, slots = create_restaurants(db, users)
    create_reservations(db, restaurants, users)
    create_reviews(db, users, restaurants)


if __name__ == "__main__":
    from dependencies.database import get_db

    db = next(get_db())
    load_mock_data(db)
    print("\nMock data loaded successfully.")
    db.close()
