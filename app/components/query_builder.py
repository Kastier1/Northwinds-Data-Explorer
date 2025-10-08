import reflex as rx
import reflex_enterprise as rxe
from app.states.base_state import BaseState
from app.states.query_builder_state import QueryBuilderState


@rx.memo
def draggable_table_card(table_name: str, **props):
    return rxe.dnd.draggable(
        rx.el.div(
            rx.icon("table", class_name="h-5 w-5 mr-2"),
            table_name,
            class_name="flex items-center p-3 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md hover:border-sky-300 transition-all cursor-grab active:cursor-grabbing",
        ),
        type="table",
        item={"id": table_name},
        **props,
    )


def table_selection_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Tables", class_name="text-lg font-semibold text-gray-700 mb-4 px-2"),
        rx.el.div(
            rx.foreach(
                BaseState.tables,
                lambda table: draggable_table_card(table_name=table, key=table),
            ),
            class_name="space-y-2",
        ),
        class_name="w-64 p-4 bg-gray-50 border-r border-gray-200 h-full overflow-y-auto",
    )


@rx.memo
def query_drop_zone():
    drop_params = rxe.dnd.DropTarget.collected_params
    return rxe.dnd.drop_target(
        rx.el.div(
            rx.el.h3(
                "Query Builder", class_name="text-lg font-semibold text-gray-700 mb-4"
            ),
            rx.el.div(
                rx.cond(
                    QueryBuilderState.dropped_tables.length() == 0,
                    rx.el.div(
                        rx.icon("move", class_name="h-8 w-8 text-gray-400 mb-2"),
                        rx.el.p(
                            "Drag tables here to build a query",
                            class_name="text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center h-full text-center p-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            QueryBuilderState.dropped_tables,
                            lambda table: rx.el.div(
                                table,
                                rx.el.button(
                                    rx.icon("x", class_name="h-4 w-4"),
                                    on_click=lambda: QueryBuilderState.remove_table(
                                        table
                                    ),
                                    class_name="ml-2 text-gray-400 hover:text-red-500",
                                ),
                                class_name="flex items-center bg-sky-100 text-sky-800 text-sm font-medium px-3 py-1.5 rounded-full",
                            ),
                        ),
                        class_name="flex flex-wrap gap-2 p-4",
                    ),
                ),
                class_name=rx.cond(
                    drop_params.is_over,
                    "h-48 border-2 border-dashed border-sky-500 rounded-lg bg-sky-50 transition-all",
                    "h-48 border-2 border-dashed border-gray-300 rounded-lg bg-white transition-all",
                ),
            ),
            class_name="flex-1 p-6",
        ),
        accept=["table"],
        on_drop=QueryBuilderState.add_table_to_query,
    )


def query_display() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Generated SQL", class_name="text-lg font-semibold text-gray-700 mb-2"
        ),
        rx.el.div(
            rx.el.code(
                QueryBuilderState.generated_sql,
                class_name="text-sm font-mono text-gray-800",
            ),
            class_name="bg-gray-100 p-4 rounded-lg overflow-x-auto",
        ),
        rx.el.div(
            rx.el.button(
                "Execute Query",
                on_click=QueryBuilderState.execute_query,
                disabled=QueryBuilderState.generated_sql == "",
                class_name="mt-4 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:bg-gray-300 disabled:cursor-not-allowed",
            ),
            rx.el.button(
                "Clear",
                on_click=QueryBuilderState.clear_query,
                class_name="mt-4 ml-2 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
            ),
        ),
        class_name="p-6",
    )


def results_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Query Results", class_name="text-lg font-semibold text-gray-700 mb-4"
        ),
        rx.cond(
            QueryBuilderState.loading,
            rx.el.div(rx.spinner(), class_name="flex justify-center p-8"),
            rx.cond(
                QueryBuilderState.error_message != "",
                rx.el.div(
                    rx.icon(
                        "flag_triangle_right", class_name="h-5 w-5 text-red-500 mr-2"
                    ),
                    QueryBuilderState.error_message,
                    class_name="flex items-center bg-red-100 text-red-700 p-4 rounded-lg",
                ),
                rx.cond(
                    QueryBuilderState.query_results.length() > 0,
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.foreach(
                                        QueryBuilderState.query_columns,
                                        lambda col: rx.el.th(
                                            col,
                                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                        ),
                                    ),
                                    class_name="bg-gray-50",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    QueryBuilderState.query_results,
                                    lambda row: rx.el.tr(
                                        rx.foreach(
                                            QueryBuilderState.query_columns,
                                            lambda col: rx.el.td(
                                                rx.cond(
                                                    row[col],
                                                    row[col].to_string(),
                                                    "N/A",
                                                ),
                                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-700",
                                            ),
                                        ),
                                        class_name="bg-white even:bg-gray-50",
                                    ),
                                ),
                                class_name="divide-y divide-gray-200",
                            ),
                            class_name="min-w-full divide-y divide-gray-200",
                        ),
                        class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg overflow-x-auto",
                    ),
                    rx.el.div(
                        "No results to display. Execute a query to see data here.",
                        class_name="text-gray-500 p-4",
                    ),
                ),
            ),
        ),
        class_name="p-6",
    )


def query_builder_page() -> rx.Component:
    return rx.el.div(
        table_selection_sidebar(),
        rx.el.div(
            query_drop_zone(),
            query_display(),
            results_table(),
            class_name="flex-1 flex flex-col",
        ),
        class_name="flex h-full",
    )