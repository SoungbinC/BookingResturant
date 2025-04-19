# adapters/google_maps_adapter.py
import urllib.parse


class GoogleMapsAdapter:
    BASE_URL = "https://www.google.com/maps/search/?api=1&query="

    def get_map_url(self, address: str):
        encoded_address = urllib.parse.quote(address)
        return f"{self.BASE_URL}{encoded_address}"


# Usage
"""
adapter = GoogleMapsAdapter()
adapter.get_map_url(restaurant.address)
"""
