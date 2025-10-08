import reflex as rx
import reflex_enterprise as rxe
from reflex_azure_auth import (
    AzureAuthState,
    azure_login_button,
    register_auth_endpoints,
)
from app.states.auth_state import AuthState
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
        rx.el.div(
            rx.el.p(rx.text(f"Welcome, {AuthState.userinfo['name']}!")),
            rx.el.button("Logout", on_click=AuthState.redirect_to_logout),
            class_name="flex items-center gap-4",
        ),
        class_name="flex items-center justify-between bg-white border-b border-gray-200 p-4 sticky top-0 z-30",
    )


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="wind", class_name="h-12 w-12 text-sky-500"),
            rx.el.h1("Northwind", class_name="text-4xl font-bold text-gray-800 mt-4"),
            rx.el.p(
                "Please log in to continue.", class_name="text-lg text-gray-600 mt-2"
            ),
            azure_login_button(
                rx.el.button(
                    "Log In with Microsoft",
                    class_name="mt-6 inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-10 px-4 py-2",
                )
            ),
            class_name="flex flex-col items-center p-8 bg-white rounded-xl shadow-lg border border-gray-200",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            rx.State.is_hydrated,
            rx.cond(
                AuthState.is_authenticated,
                rx.el.div(
                    sidebar(),
                    rx.el.main(
                        header(),
                        data_table(),
                        class_name=rx.cond(
                            BaseState.is_sidebar_open,
                            "transition-all sm:ml-64",
                            "transition-all",
                        ),
                    ),
                    class_name="min-h-screen bg-gray-50 font-['Open_Sans']",
                ),
                login_page(),
            ),
            rx.el.div(
                rx.spinner(class_name="text-sky-500 h-8 w-8"),
                class_name="flex items-center justify-center min-h-screen",
            ),
        )
    )


app = rxe.App(
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
app.add_page(index, on_load=[AuthState.on_load, DataTableState.fetch_data])
register_auth_endpoints(app)