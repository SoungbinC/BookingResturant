from sqlalchemy.orm import Query
from sqlalchemy import func
from models import Restaurant, BookingSlot
from typing import Optional
from patterns.strategy import SearchStrategy


class NameSearchStrategy(SearchStrategy):
    def apply(self, query: Query, value: Optional[str]):
        if value:
            return query.filter(Restaurant.name.ilike(f"%{value}%"))
        return query


class CuisineSearchStrategy(SearchStrategy):
    def apply(self, query: Query, value: Optional[str]):
        if value:
            cuisines = [v.strip() for v in value.split(",")]
            for cuisine in cuisines:
                query = query.filter(Restaurant.cuisine.ilike(f"%{cuisine}%"))
        return query


class CitySearchStrategy(SearchStrategy):
    def apply(self, query: Query, value: Optional[str]):
        if value:
            return query.filter(Restaurant.city.ilike(f"%{value}%"))
        return query


class ZipcodeSearchStrategy(SearchStrategy):
    def apply(self, query: Query, value: Optional[str]):
        if value:
            return query.filter(Restaurant.zipcode.ilike(f"%{value}%"))
        return query


class TimeWindowSlotStrategy(SearchStrategy):
    def apply(self, query: Query, time_window: tuple):
        start, end = time_window

        # Subquery to find restaurant_ids that have unbooked slots in the given time window
        available_slot_restaurant_ids = (
            query.session.query(Restaurant.id)
            .join(Restaurant.booking_slots)
            .filter(
                BookingSlot.is_booked == False,
                BookingSlot.start_time >= start,
                BookingSlot.start_time <= end,
            )
            .distinct()
            .subquery()
        )

        return query.filter(Restaurant.id.in_(available_slot_restaurant_ids))


# ===========================================


class SearchContext:
    def __init__(self, strategies: list):
        self.strategies = strategies

    def apply_filters(self, query):
        for strategy, value in self.strategies:
            # Each strategy applies independently and accumulates results
            query = strategy.apply(query, value)
        return query
