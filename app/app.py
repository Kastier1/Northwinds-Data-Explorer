import reflex as rx
from app.components.sidebar import sidebar
from app.components.data_table import data_table
from app.states.base_state import BaseState
from app.states.data_table_state import DataTableState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(tag="menu", class_name="h-6 w-6"),
                on_click=BaseState.toggle_sidebar,
                class_name="p-2 text-gray-600 hover:bg-gray-100 rounded-lg sm:hidden",
            ),
            rx.el.h1(
                f"Northwind / {BaseState.active_table}",
                class_name="text-2xl font-semibold text-gray-800",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="bg-white border-b border-gray-200 p-4 sticky top-0 z-30",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            data_table(),
            class_name=rx.cond(
                BaseState.is_sidebar_open, "transition-all sm:ml-64", "transition-all"
            ),
        ),
        class_name="min-h-screen bg-gray-50 font-['Open_Sans']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=DataTableState.fetch_data)