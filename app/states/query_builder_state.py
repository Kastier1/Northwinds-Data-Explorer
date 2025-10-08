import reflex as rx
import reflex_enterprise as rxe
from typing import Union, cast
from reflex_enterprise.components.flow.types import Node, Edge
from sqlalchemy import text
import logging
from .base_state import BaseState


class QueryBuilderState(rx.State):
    """State for the SQL query builder."""

    selected_tables: list[str] = []
    generated_sql: str = ""
    query_results: list[dict[str, Union[str, int, float, bool, bytes, None]]] = []
    query_columns: list[str] = []
    loading: bool = False
    error_message: str = ""
    nodes: list[Node] = []
    edges: list[Edge] = []
    TABLE_RELATIONSHIPS = {
        "Orders": [
            {"target": "Customers", "on": "CustomerID"},
            {"target": "Employees", "on": "EmployeeID"},
            {"target": "Shippers", "on": "ShipVia", "target_on": "ShipperID"},
        ],
        "Order Details": [
            {"target": "Orders", "on": "OrderID"},
            {"target": "Products", "on": "ProductID"},
        ],
        "Products": [
            {"target": "Suppliers", "on": "SupplierID"},
            {"target": "Categories", "on": "CategoryID"},
        ],
        "Employees": [
            {"target": "Employees", "on": "ReportsTo", "target_on": "EmployeeID"}
        ],
    }

    @rx.event(background=True)
    async def on_load(self):
        """Initialize nodes and edges on page load."""
        async with self:
            base_state = await self.get_state(BaseState)
            tables = base_state.tables
            self.nodes, self.edges = self._create_flow_elements(tables)

    def _create_flow_elements(self, tables: list[str]) -> tuple[list[Node], list[Edge]]:
        """Create nodes and edges for the flow diagram."""
        nodes: list[Node] = []
        edges: list[Edge] = []
        grid_cols = 4
        x_spacing = 200
        y_spacing = 150
        for idx, table_name in enumerate(tables):
            col = idx % grid_cols
            row = idx // grid_cols
            nodes.append(
                {
                    "id": table_name,
                    "type": "default",
                    "data": {"label": table_name},
                    "position": {"x": col * x_spacing, "y": row * y_spacing},
                    "style": {
                        "border": "1px solid #777",
                        "padding": "10px",
                        "borderRadius": "8px",
                        "background": "#f9f9f9",
                    },
                }
            )
        edge_id = 0
        for source_table, relations in self.TABLE_RELATIONSHIPS.items():
            for rel in relations:
                target_table = rel["target"]
                source_on = rel["on"]
                target_on = rel.get("target_on", source_on)
                edges.append(
                    {
                        "id": f"e{edge_id}",
                        "source": source_table,
                        "target": target_table,
                        "type": "smoothstep",
                        "animated": True,
                        "label": f"{source_on} -> {target_on}",
                    }
                )
                edge_id += 1
        return (nodes, edges)

    @rx.event
    def handle_node_click(self, node: Node):
        """Handle clicking a node to select or deselect a table."""
        node_id = cast(str, node["id"])
        if node_id in self.selected_tables:
            self.selected_tables.remove(node_id)
        else:
            self.selected_tables.append(node_id)
        for i, n in enumerate(self.nodes):
            if n["id"] == node_id:
                is_selected = node_id in self.selected_tables
                self.nodes[i]["style"] = {
                    "border": f"2px solid {('#3b82f6' if is_selected else '#777')}",
                    "padding": "10px",
                    "borderRadius": "8px",
                    "background": f"{('#dbeafe' if is_selected else '#f9f9f9')}",
                    "fontWeight": f"{('600' if is_selected else '400')}",
                }
                break
        self._construct_sql()

    @rx.event
    def clear_query(self):
        """Clear the query builder."""
        self.selected_tables = []
        self.generated_sql = ""
        self.query_results = []
        self.query_columns = []
        self.error_message = ""
        for i in range(len(self.nodes)):
            self.nodes[i]["style"] = {
                "border": "1px solid #777",
                "padding": "10px",
                "borderRadius": "8px",
                "background": "#f9f9f9",
                "fontWeight": "400",
            }

    def _construct_sql(self):
        """Construct a SQL query based on selected tables."""
        if not self.selected_tables:
            self.generated_sql = ""
            return
        tables = self.selected_tables
        if len(tables) == 1:
            self.generated_sql = f'SELECT TOP 100 * FROM "{tables[0]}"'
            return
        query_parts = [f'SELECT TOP 100 * FROM "{tables[0]}"']
        joined_tables = {tables[0]}
        tables_to_join_queue = list(tables[1:])
        while tables_to_join_queue:
            table_to_join = tables_to_join_queue.pop(0)
            join_found = False
            for existing_table in joined_tables:
                if existing_table in self.TABLE_RELATIONSHIPS:
                    for rel in self.TABLE_RELATIONSHIPS[existing_table]:
                        if rel["target"] == table_to_join:
                            source_on = rel["on"]
                            target_on = rel.get("target_on", source_on)
                            condition = f'"{existing_table}"."{source_on}" = "{table_to_join}"."{target_on}"'
                            query_parts.append(
                                f'LEFT JOIN "{table_to_join}" ON {condition}'
                            )
                            join_found = True
                            break
                if not join_found and table_to_join in self.TABLE_RELATIONSHIPS:
                    for rel in self.TABLE_RELATIONSHIPS[table_to_join]:
                        if rel["target"] == existing_table:
                            source_on = rel["on"]
                            target_on = rel.get("target_on", source_on)
                            condition = f'"{table_to_join}"."{source_on}" = "{existing_table}"."{target_on}"'
                            query_parts.append(
                                f'LEFT JOIN "{table_to_join}" ON {condition}'
                            )
                            join_found = True
                            break
                if join_found:
                    break
            if join_found:
                joined_tables.add(table_to_join)
            else:
                tables_to_join_queue.append(table_to_join)
                if len(tables_to_join_queue) > len(tables) ** 2:
                    for unjoined_table in tables_to_join_queue:
                        query_parts.append(f'CROSS JOIN "{unjoined_table}"')
                    break
        self.generated_sql = " ".join(query_parts)

    @rx.event(background=True)
    async def execute_query(self):
        """Execute the generated SQL query."""
        if not self.generated_sql:
            return
        async with self:
            self.loading = True
            self.error_message = ""
            self.query_results = []
            self.query_columns = []
        try:
            async with rx.asession() as session:
                result = await session.execute(text(self.generated_sql))
                rows = result.mappings().all()
                async with self:
                    if rows:
                        self.query_columns = list(rows[0].keys())
                        self.query_results = [dict(row) for row in rows]
                    self.loading = False
        except Exception as e:
            logging.exception(f"Error executing query: {e}")
            async with self:
                self.error_message = f"Query failed: {str(e)}"
                self.loading = False