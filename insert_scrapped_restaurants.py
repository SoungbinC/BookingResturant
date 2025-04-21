from pathlib import Path
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.restaurant import Restaurant
from models.review import Review
from models.user import User, UserRole
from dependencies.database import Database
import re
from collections import defaultdict


day_aliases = {
    "mon": "open_mon",
    "tue": "open_tue",
    "wed": "open_wed",
    "thu": "open_thu",
    "fri": "open_fri",
    "sat": "open_sat",
    "sun": "open_sun",
}


# -----------------------
# 🔁 Expand day ranges
# -----------------------
def expand_day_range(day_range):
    days = list(day_aliases.keys())
    parts = [d.strip().lower()[:3] for d in day_range.replace("–", "-").split("-")]
    if len(parts) == 1:
        return [day_aliases.get(parts[0])]
    if parts[0] in days and parts[1] in days:
        start, end = days.index(parts[0]), days.index(parts[1])
        return [day_aliases[d] for d in days[start : end + 1]]
    return []


# -----------------------
# 🕒 Parse hours text
# -----------------------
def parse_opening_hours_fixed(hours_text):
    schedule = defaultdict(lambda: None)
    normalized = hours_text.replace("–", "-")
    parts = re.split(r";|\n", normalized)

    for part in parts:
        part = part.strip()

        # Remove shift label (e.g., Lunch:, Dinner:, etc.)
        prefix_match = re.match(
            r"^(Lunch|Dinner|Brunch|Bar|Breakfast|Lunch and Dinner):?\s*",
            part,
            flags=re.IGNORECASE,
        )
        if prefix_match:
            part = part[prefix_match.end() :]

        # Match "Days 10:00 am - 2:00 pm"
        match = re.search(
            r"([A-Za-z,\s\-]+):?\s*(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)",
            part,
        )
        if match:
            day_str, start, end = match.groups()
            time_range = f"{start}-{end}"
            if "daily" in day_str.lower() or "sunday - saturday" in day_str.lower():
                for k in day_aliases.values():
                    schedule[k] = time_range
            else:
                for section in day_str.split(","):
                    keys = expand_day_range(section.strip())
                    for k in keys:
                        schedule[k] = time_range

    return dict(schedule)


# Load data
json_path = Path("scraped_restaurants.json")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Initialize DB session
db: Session = Database.get_instance().SessionLocal()
user_cache = {}

for entry in data:
    # Avoid inserting duplicate restaurants
    existing_restaurant = db.query(Restaurant).filter_by(name=entry["name"]).first()
    if existing_restaurant:
        print(f"⚠️ Restaurant '{entry['name']}' already exists. Skipping.")
        continue

    # Address parsing
    address_parts = entry["address"].split(",")
    city = address_parts[-2].strip() if len(address_parts) >= 2 else None
    state_zip = (
        address_parts[-1].strip().split(" ") if len(address_parts) > 1 else ["", ""]
    )
    state = state_zip[0] if len(state_zip) > 0 else None
    zipcode = state_zip[1] if len(state_zip) > 1 else None

    # Parse hours
    parsed_hours = parse_opening_hours_fixed(entry.get("hours", ""))
    print(f'before parsed hours for {entry["name"]}: {entry.get("hours")}')
    print(f'⏰ Parsed hours for {entry["name"]}: {parsed_hours}')

    # Create restaurant
    restaurant = Restaurant(
        name=entry["name"],
        description=entry.get("description"),
        address=entry["address"],
        map_url=entry.get("map_url"),
        city=city,
        state=state,
        zipcode=zipcode,
        cuisine=entry.get("cuisine"),
        price_range=entry.get("price"),
        rating=(
            float(entry["rating"])
            if entry.get("rating") not in [None, "Unknown", ""]
            else None
        ),
        photo_url=entry.get("photo_url"),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        open_mon=parsed_hours.get("open_mon"),
        open_tue=parsed_hours.get("open_tue"),
        open_wed=parsed_hours.get("open_wed"),
        open_thu=parsed_hours.get("open_thu"),
        open_fri=parsed_hours.get("open_fri"),
        open_sat=parsed_hours.get("open_sat"),
        open_sun=parsed_hours.get("open_sun"),
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    for review in entry.get("reviews", []):
        reviewer_name = review["reviewer"]
        reviewer_email = f"{reviewer_name.lower().replace(' ', '_')}@example.com"

        user = user_cache.get(reviewer_name)
        if not user:
            user = (
                db.query(User)
                .filter(
                    or_(User.username == reviewer_name, User.email == reviewer_email)
                )
                .first()
            )
            if not user:
                user = User(
                    username=reviewer_name,
                    email=reviewer_email,
                    hashed_password="not_real_hash",
                    role=UserRole.CUSTOMER,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            user_cache[reviewer_name] = user

        db_review = Review(
            user_id=user.id,
            restaurant_id=restaurant.id,
            rating=int(review["rating"]),
            comment=review["text"][:500],
        )
        db.add(db_review)

    db.commit()


# Find and delete restaurants missing all open_* fields
to_delete = []
for r in db.query(Restaurant).all():
    if all(getattr(r, field) is None for field in day_aliases.values()):
        # Check if restaurant has any reviews
        has_reviews = db.query(Review).filter(Review.restaurant_id == r.id).count() > 0
        if has_reviews:

            print(f"❌ Deleting restaurant with reviews: {r.id} - {r.name}")
            to_delete.append(r)
            continue
        # Check if restaurant has any bookings
        print(f"❌ Deleting restaurant: {r.id} - {r.name}")
        to_delete.append(r)

for r in to_delete:
    print(
        f"❌ Deleting reviews and any related bookings for restaurant: {r.id} - {r.name}"
    )
    db.query(Review).filter(Review.restaurant_id == r.id).delete()

    db.delete(r)


print("✅ Finished inserting all data with parsed open hours.")
db.close()
