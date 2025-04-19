from patterns.strategy import SearchStrategy
from models import Restaurant, BookingSlot
from typing import List, Tuple
from datetime import datetime
from sqlalchemy.orm import aliased

# Search List
# ===========================================


class NameSearchStrategy(SearchStrategy):
    def apply(self, query, value):
        if value:
            return query.filter(Restaurant.name.ilike(f"%{value}%"))
        return query


class CitySearchStrategy(SearchStrategy):
    def apply(self, query, value):
        if value:
            return query.filter(Restaurant.city.ilike(f"%{value}%"))
        return query


class ZipSearchStrategy(SearchStrategy):
    def apply(self, query, value):
        if value:
            return query.filter(Restaurant.zipcode == value)
        return query


class CuisineSearchStrategy(SearchStrategy):
    def apply(self, query, value):
        if value:
            return query.filter(Restaurant.cuisine.ilike(f"%{value}%"))
        return query


class TimeWindowSlotStrategy(SearchStrategy):
    def apply(self, query, time_window: tuple):
        start, end = time_window

        # Subquery to find restaurant_ids that have unbooked slots in time window
        available_slot_restaurant_ids = (
            query.session.query(BookingSlot.restaurant_id)
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
    def __init__(self, strategies: List[Tuple[SearchStrategy, str]]):
        self.strategies = strategies

    def apply_filters(self, query):
        for strategy, value in self.strategies:
            query = strategy.apply(query, value)
        return query
