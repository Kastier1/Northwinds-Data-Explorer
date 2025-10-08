import reflex as rx
import reflex_enterprise as rxe
from app.states.query_builder_state import QueryBuilderState
from .flow import schema_flow_component


def query_controls() -> rx.Component:
    """Controls for the query builder: execute, clear, and SQL display."""
    return rx.el.div(
        rx.el.h3(
            "Generated SQL", class_name="text-lg font-semibold text-gray-700 mb-2"
        ),
        rx.el.div(
            rx.el.code(
                QueryBuilderState.generated_sql,
                class_name="text-sm font-mono text-gray-800",
            ),
            class_name="bg-gray-100 p-4 rounded-lg overflow-x-auto min-h-[60px]",
        ),
        rx.el.div(
            rx.el.button(
                "Execute Query",
                on_click=QueryBuilderState.execute_query,
                disabled=QueryBuilderState.generated_sql == "",
                class_name="mt-4 px-4 py-2 bg-sky-600 text-white rounded-lg hover:bg-sky-700 disabled:bg-gray-300 disabled:cursor-not-allowed",
            ),
            rx.el.button(
                "Clear Selection",
                on_click=QueryBuilderState.clear_query,
                class_name="mt-4 ml-2 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300",
            ),
            class_name="flex items-center",
        ),
        class_name="p-4 border-t border-gray-200",
    )


def results_table() -> rx.Component:
    """Displays the results of the executed SQL query."""
    return rx.el.div(
        rx.el.h3(
            "Query Results", class_name="text-lg font-semibold text-gray-700 mb-4"
        ),
        rx.cond(
            QueryBuilderState.loading,
            rx.el.div(
                rx.spinner(class_name="text-sky-500"),
                class_name="flex justify-center items-center p-8 h-full",
            ),
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
                                                    row[col] != None,
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
                        class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg overflow-auto",
                    ),
                    rx.el.div(
                        "Click on table nodes to build a query, then click 'Execute Query'.",
                        class_name="text-gray-500 p-8 text-center",
                    ),
                ),
            ),
        ),
        class_name="p-6 flex-1",
    )


def query_builder_page() -> rx.Component:
    """The main page for the query builder, combining the flow diagram and results."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Database Schema", class_name="text-xl font-semibold p-4"),
            rx.el.p(
                "Click on tables to add them to your query.",
                class_name="px-4 pb-4 text-gray-500 text-sm",
            ),
            schema_flow_component(),
            query_controls(),
            class_name="w-1/2 flex flex-col border-r border-gray-200 bg-white",
        ),
        rx.el.div(results_table(), class_name="w-1/2 flex flex-col bg-gray-50"),
        class_name="flex h-[calc(100vh-65px)]",
    )