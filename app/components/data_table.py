import reflex as rx
import reflex_enterprise as rxe
from app.states.data_table_state import DataTableState


def data_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
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
                class_name="px-4 py-4 sm:px-6 lg:px-8",
            ),
            rx.el.div(
                rxe.ag_grid(
                    id="data_table_grid",
                    column_defs=DataTableState.column_defs,
                    row_data=DataTableState.table_data,
                    quick_filter_text=DataTableState.search_query,
                    pagination=True,
                    pagination_page_size=10,
                    theme="quartz",
                    dom_layout="autoHeight",
                ),
                class_name="w-full",
            ),
            class_name="bg-white border rounded-lg shadow-sm",
        ),
        class_name="p-4 sm:p-6 lg:p-8",
    )