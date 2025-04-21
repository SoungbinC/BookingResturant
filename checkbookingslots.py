from sqlalchemy.orm import Session
from models.restaurant import Restaurant
from models.bookingslot import BookingSlot
from dependencies.database import Database
from datetime import datetime

db: Session = Database.get_instance().SessionLocal()

# Find all restaurants without any booking slots
restaurants_without_slots = (
    db.query(Restaurant)
    .filter(Restaurant.name != "Unknown")
    .outerjoin(BookingSlot)
    .filter(BookingSlot.id.is_(None))
    .all()
)

print(f"🚫 Restaurants without booking slots ({len(restaurants_without_slots)}):")
for r in restaurants_without_slots:
    print(f"- {r.id}: {r.name}")

db.close()


day_column_map = {
    0: "open_mon",
    1: "open_tue",
    2: "open_wed",
    3: "open_thu",
    4: "open_fri",
    5: "open_sat",
    6: "open_sun",
}


def parse_time_range(time_str):
    try:
        start_str, end_str = [x.strip() for x in time_str.split("-")]
        start_time = datetime.strptime(start_str, "%I:%M %p").time()
        end_time = datetime.strptime(end_str, "%I:%M %p").time()
        return start_time, end_time
    except Exception:
        return None, None


def check_restaurant_time_availability(restaurant):
    for i in range(7):
        column = day_column_map[i]
        time_range = getattr(restaurant, column)
        if time_range and "-" in time_range:
            start, end = parse_time_range(time_range)
            if start and end and start < end:
                return True
    return False


db: Session = Database.get_instance().SessionLocal()
restaurants = db.query(Restaurant).all()

print("\n🚫 Restaurants with NO valid open hours:")
for r in restaurants:
    if not check_restaurant_time_availability(r):
        print(f"- {r.id}: {r.name}")
        for day, col in day_column_map.items():
            print(f"  {col}: {getattr(r, col)}")

db.close()
