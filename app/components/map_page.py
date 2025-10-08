import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.map_state import MapState


def map_page() -> rx.Component:
    """The customer map page."""
    return rx.el.div(
        rx.cond(
            MapState.loading,
            rx.el.div(
                rx.spinner(class_name="h-12 w-12 text-sky-600"),
                rx.el.p(
                    "Loading customer locations...", class_name="mt-4 text-gray-600"
                ),
                class_name="flex flex-col items-center justify-center h-full",
            ),
            rx.cond(
                MapState.error != "",
                rx.el.div(
                    rx.icon("flag_triangle_right", class_name="h-12 w-12 text-red-500"),
                    rx.el.p(MapState.error, class_name="mt-4 text-red-600"),
                    class_name="flex flex-col items-center justify-center h-full",
                ),
                rxe.map(
                    rxe.map.tile_layer(
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    ),
                    rx.foreach(
                        MapState.locations,
                        lambda location: rxe.map.marker(
                            rxe.map.popup(
                                rx.el.div(
                                    rx.el.p(
                                        location["customer_name"],
                                        class_name="font-bold",
                                    ),
                                    rx.el.p(
                                        f"{location['city']}, {location['country']}"
                                    ),
                                )
                            ),
                            position=latlng(lat=location["lat"], lng=location["lng"]),
                        ),
                    ),
                    id="customer_map",
                    center=MapState.center,
                    zoom=MapState.zoom,
                    height="100%",
                    width="100%",
                ),
            ),
        ),
        class_name="h-[calc(100vh-100px)] w-full p-4 sm:p-6 lg:p-8",
    )