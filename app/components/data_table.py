import reflex as rx
from app.states.data_table_state import DataTableState
from app.states.base_state import BaseState


def table_header() -> rx.Component:
    return rx.el.thead(
        rx.el.tr(
            rx.foreach(
                DataTableState.columns,
                lambda col: rx.el.th(
                    col,
                    scope="col",
                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                ),
            ),
            class_name="bg-gray-50",
        )
    )


def table_row(row_data: dict) -> rx.Component:
    return rx.el.tr(
        rx.foreach(
            DataTableState.columns,
            lambda col: rx.el.td(
                rx.cond(row_data[col], row_data[col].to_string(), "N/A"),
                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700 max-w-xs truncate",
            ),
        ),
        class_name="bg-white even:bg-gray-50 hover:bg-sky-50",
    )


def pagination_controls() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.p(
                "Showing ",
                rx.el.span(
                    (DataTableState.current_page - 1) * DataTableState.items_per_page
                    + 1,
                    class_name="font-medium",
                ),
                " to ",
                rx.el.span(
                    rx.cond(
                        DataTableState.current_page * DataTableState.items_per_page
                        > DataTableState.total_items,
                        DataTableState.total_items,
                        DataTableState.current_page * DataTableState.items_per_page,
                    ),
                    class_name="font-medium",
                ),
                " of ",
                rx.el.span(DataTableState.total_items, class_name="font-medium"),
                " results",
                class_name="text-sm text-gray-700",
            )
        ),
        rx.el.div(
            rx.el.button(
                "Previous",
                on_click=DataTableState.prev_page,
                disabled=DataTableState.current_page <= 1,
                class_name="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.el.button(
                "Next",
                on_click=DataTableState.next_page,
                disabled=DataTableState.current_page >= DataTableState.total_pages,
                class_name="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="flex",
        ),
        class_name="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6",
    )


def data_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Search...",
                    on_change=DataTableState.set_search_query.debounce(300),
                    class_name="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-sky-600 sm:text-sm sm:leading-6 pl-10",
                ),
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                class_name="relative",
            ),
            class_name="px-4 sm:px-6 lg:px-8 py-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    table_header(),
                    rx.el.tbody(rx.foreach(DataTableState.paged_data, table_row)),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                rx.cond(
                    DataTableState.loading,
                    rx.el.div(
                        rx.el.div(
                            rx.spinner(class_name="text-sky-500"),
                            class_name="flex items-center justify-center p-8",
                        ),
                        class_name="absolute inset-0 bg-white/80 backdrop-blur-sm",
                    ),
                ),
                class_name="relative overflow-x-auto",
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
        ),
        pagination_controls(),
        class_name="flex flex-col",
    )