import reflex as rx
import reflex_enterprise as rxe
from app.states.query_builder_state import QueryBuilderState


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
                        rxe.ag_grid(
                            id="query_results_grid",
                            column_defs=QueryBuilderState.query_column_defs,
                            row_data=QueryBuilderState.query_results,
                            pagination=True,
                            pagination_page_size=10,
                            theme="quartz",
                        ),
                        class_name="h-[600px] w-full",
                    ),
                    rx.el.div(
                        "No results to display. Click on tables to build a query, then execute it.",
                        class_name="text-gray-500 p-4",
                    ),
                ),
            ),
        ),
        class_name="p-6",
    )


def flow_component() -> rx.Component:
    return rx.el.div(
        rxe.flow.provider(
            rxe.flow(
                rxe.flow.background(
                    variant="dots", gap=24, size=1, class_name="bg-gray-50"
                ),
                nodes=QueryBuilderState.nodes,
                edges=QueryBuilderState.edges,
                on_node_click=QueryBuilderState.handle_node_click,
                fit_view=True,
                fit_view_options={"padding": 0.1},
                nodes_draggable=True,
                nodes_connectable=False,
                elements_selectable=True,
                color_mode="light",
            )
        ),
        class_name="h-[400px] w-full border rounded-lg bg-white",
    )


def query_builder_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Database Schema", class_name="text-lg font-semibold text-gray-700 mb-4"
            ),
            flow_component(),
            class_name="p-6",
        ),
        query_display(),
        results_table(),
        class_name="flex-1 flex flex-col h-full",
    )