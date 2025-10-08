import reflex as rx
from typing import TypedDict, Union
from sqlalchemy import text
import asyncio
import logging
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from reflex_enterprise.components.map.types import LatLng, latlng


class Location(TypedDict):
    lat: float
    lng: float
    customer_name: str
    city: str
    country: str


class MapState(rx.State):
    """State for the customer map."""

    locations: list[Location] = []
    loading: bool = False
    error: str = ""
    center: LatLng = latlng(lat=20, lng=0)
    zoom: float = 2.0

    @rx.event(background=True)
    async def fetch_customer_locations(self):
        """Fetch customer locations and geocode them."""
        async with self:
            if self.locations:
                return
            self.loading = True
            self.error = ""
        try:
            geolocator = Nominatim(user_agent="northwind_reflex_app")
            geocode = RateLimiter(
                geolocator.geocode, min_delay_seconds=1.1, error_wait_seconds=5.0
            )
            async with rx.asession() as session:
                query = text(
                    'SELECT "CompanyName", "City", "Country", "Address" FROM "Customers"'
                )
                result = await session.execute(query)
                customers = result.mappings().all()
            geocoded_locations = []
            for customer in customers:
                full_address = (
                    f"{customer['Address']}, {customer['City']}, {customer['Country']}"
                )
                try:
                    location = await asyncio.to_thread(geocode, full_address)
                    if location:
                        geocoded_locations.append(
                            {
                                "lat": location.latitude,
                                "lng": location.longitude,
                                "customer_name": customer["CompanyName"],
                                "city": customer["City"],
                                "country": customer["Country"],
                            }
                        )
                except Exception as e:
                    logging.exception(
                        f"Could not geocode address '{full_address}': {e}"
                    )
            async with self:
                self.locations = geocoded_locations
                self.loading = False
        except Exception as e:
            logging.exception(f"Error fetching customer locations: {e}")
            async with self:
                self.error = "Failed to load customer locations."
                self.loading = False