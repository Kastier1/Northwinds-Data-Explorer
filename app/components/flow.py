import reflex as rx
import reflex_enterprise as rxe
from app.states.query_builder_state import QueryBuilderState


def schema_flow_component() -> rx.Component:
    """A React Flow component to display the database schema."""
    return rx.el.div(
        rxe.flow.provider(
            rxe.flow(
                rxe.flow.background(variant="dots", gap=24, size=1),
                rxe.flow.controls(),
                nodes=QueryBuilderState.nodes,
                edges=QueryBuilderState.edges,
                on_node_click=lambda _, node: QueryBuilderState.handle_node_click(node),
                fit_view=True,
                fit_view_options={"padding": 0.1},
                nodes_draggable=True,
                nodes_connectable=False,
                edges_reconnectable=False,
                class_name="bg-white",
            )
        ),
        class_name="h-full w-full",
        style={"height": "calc(100% - 140px)"},
    )