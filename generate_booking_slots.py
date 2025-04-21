from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.restaurant import Restaurant
from models.bookingslot import BookingSlot
from dependencies.database import Database

# Mapping day index (0=Mon) to restaurant open_xxx fields
day_column_map = {
    0: "open_mon",
    1: "open_tue",
    2: "open_wed",
    3: "open_thu",
    4: "open_fri",
    5: "open_sat",
    6: "open_sun",
}


def normalize_time_format(time_str):
    """Ensure there's a space between time and meridian (e.g., '5:00pm' → '5:00 pm')"""
    try:
        parts = time_str.strip().split("-")
        if len(parts) != 2:
            return time_str
        start = parts[0].strip()
        end = parts[1].strip()
        if " " not in start:
            start = f"{start[:-2]} {start[-2:]}"
        if " " not in end:
            end = f"{end[:-2]} {end[-2:]}"
        return f"{start}-{end}"
    except Exception:
        return time_str


def parse_time_range(time_str):
    try:
        start_str, end_str = [x.strip() for x in time_str.split("-")]
        start_time = datetime.strptime(start_str, "%I:%M %p").time()
        end_time = datetime.strptime(end_str, "%I:%M %p").time()
        return start_time, end_time
    except Exception:
        return None, None


def create_slots_for_restaurant(
    db: Session, restaurant: Restaurant, days_ahead: int = 7
):
    today = datetime.now()
    slot_count = 0

    for offset in range(days_ahead):
        current_date = today + timedelta(days=offset)
        column = day_column_map[current_date.weekday()]
        time_range = getattr(restaurant, column)

        if not time_range or "-" not in time_range:
            continue

        normalized_range = normalize_time_format(time_range)
        start_time, end_time = parse_time_range(normalized_range)
        if not start_time or not end_time:
            continue

        slot_start = datetime.combine(current_date.date(), start_time)
        slot_end = datetime.combine(current_date.date(), end_time)

        while slot_start + timedelta(minutes=30) <= slot_end:
            slot = BookingSlot(
                restaurant_id=restaurant.id,
                start_time=slot_start,
                end_time=slot_start + timedelta(minutes=30),
                is_booked=False,
                table_size=4,
            )
            db.add(slot)
            slot_start += timedelta(minutes=30)
            slot_count += 1

    return slot_count


def generate_all_booking_slots():
    db: Session = Database.get_instance().SessionLocal()

    # 🔁 Clear existing booking slots first
    deleted = db.query(BookingSlot).delete()
    db.commit()
    print(f"🧹 Deleted {deleted} existing booking slots.")

    # 🛠 Generate new booking slots
    restaurants = db.query(Restaurant).all()
    total_slots = 0

    for restaurant in restaurants:
        count = create_slots_for_restaurant(db, restaurant)
        total_slots += count

    db.commit()
    db.close()
    print(f"✅ Generated {total_slots} 30-minute booking slots.")


if __name__ == "__main__":
    generate_all_booking_slots()
