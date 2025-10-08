import reflex as rx
from app.states.base_state import BaseState
from app.states.data_table_state import DataTableState


def sidebar_item(
    text: str, is_active: bool, href: str, on_click_event, icon_tag: str = "layout-grid"
) -> rx.Component:
    return rx.el.li(
        rx.el.a(
            rx.el.div(
                rx.icon(tag=icon_tag, class_name="mr-3 h-5 w-5"),
                text,
                class_name="flex items-center",
            ),
            href=href,
            on_click=on_click_event,
            class_name=rx.cond(
                is_active,
                "flex items-center p-2 text-gray-900 rounded-lg bg-sky-100 font-semibold",
                "flex items-center p-2 text-gray-700 rounded-lg hover:bg-gray-100",
            ),
        )
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(tag="wind", class_name="h-8 w-8 text-sky-500"),
                    rx.el.h1(
                        "Northwind", class_name="text-2xl font-bold text-gray-800 ml-2"
                    ),
                    class_name="flex items-center p-4",
                ),
                rx.el.ul(
                    sidebar_item(
                        "Query Builder",
                        BaseState.active_table == "Query Builder",
                        "/query-builder",
                        lambda: BaseState.set_active_table("Query Builder"),
                        icon_tag="binary",
                    ),
                    sidebar_item(
                        "Customer Map",
                        BaseState.active_table == "Customer Map",
                        "/customer-map",
                        lambda: BaseState.set_active_table("Customer Map"),
                        icon_tag="map",
                    ),
                    rx.el.hr(class_name="my-2"),
                    rx.foreach(
                        BaseState.tables,
                        lambda table: sidebar_item(
                            table,
                            BaseState.active_table == table,
                            "/",
                            lambda: DataTableState.set_active_table_and_fetch(table),
                        ),
                    ),
                    class_name="space-y-2 font-medium",
                ),
                class_name="h-full px-3 py-4 overflow-y-auto bg-white border-r border-gray-200",
            ),
            class_name="h-full",
        ),
        class_name=rx.cond(
            BaseState.is_sidebar_open,
            "fixed top-0 left-0 z-40 w-64 h-screen transition-transform",
            "fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0",
        ),
        aria_label="Sidebar",
    )