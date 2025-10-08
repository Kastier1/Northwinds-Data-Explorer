import reflex as rx
from typing import Any, Union
from sqlalchemy import text
import logging
import reflex_enterprise as rxe
from reflex_enterprise.components.flow.types import Node, Edge


class QueryBuilderState(rx.State):
    """State for the SQL query builder."""

    generated_sql: str = ""
    query_results: list[dict[str, Union[str, int, float, bool, bytes, None]]] = []
    query_columns: list[str] = []
    loading: bool = False
    error_message: str = ""
    nodes: list[Node] = []
    edges: list[Edge] = []
    selected_tables: list[str] = []
    RELATIONSHIPS: dict[str, str] = {
        "Orders-Customers": "Orders.CustomerID = Customers.CustomerID",
        "Orders-Employees": "Orders.EmployeeID = Employees.EmployeeID",
        "Orders-Shippers": "Orders.ShipVia = Shippers.ShipperID",
        "Order Details-Orders": '"Order Details".OrderID = Orders.OrderID',
        "Order Details-Products": '"Order Details".ProductID = Products.ProductID',
        "Products-Categories": "Products.CategoryID = Categories.CategoryID",
        "Products-Suppliers": "Products.SupplierID = Suppliers.SupplierID",
    }

    @rx.event
    def on_load(self):
        """Initialize nodes and edges for the flow component."""
        tables = [
            "Employees",
            "Categories",
            "Customers",
            "Shippers",
            "Suppliers",
            "Orders",
            "Products",
            "Order Details",
        ]
        initial_nodes = []
        grid_cols = 4
        spacing_x = 220
        spacing_y = 120
        for i, table in enumerate(tables):
            row = i // grid_cols
            col = i % grid_cols
            initial_nodes.append(
                {
                    "id": table,
                    "type": "default",
                    "data": {"label": table},
                    "position": {"x": col * spacing_x, "y": row * spacing_y},
                    "style": {
                        "border": "1px solid #777",
                        "padding": "10px",
                        "background": "white",
                        "borderRadius": "8px",
                    },
                }
            )
        self.nodes = initial_nodes
        initial_edges = []
        for i, key in enumerate(self.RELATIONSHIPS.keys()):
            source, target = key.split("-")
            initial_edges.append(
                {
                    "id": f"edge-{i}",
                    "source": source,
                    "target": target,
                    "type": "smoothstep",
                    "animated": False,
                    "style": {"stroke": "#aaa"},
                }
            )
        self.edges = initial_edges

    @rx.event
    def handle_node_click(self, node: Node):
        """Handle node click to select/deselect tables and construct query."""
        node_id = node["id"]
        if node_id in self.selected_tables:
            self.selected_tables.remove(node_id)
        else:
            self.selected_tables.append(node_id)
        for i, n in enumerate(self.nodes):
            if n["id"] == node_id:
                is_selected = n["id"] in self.selected_tables
                self.nodes[i]["style"] = {
                    "border": f"2px solid {('#2563eb' if is_selected else '#777')}",
                    "padding": "10px",
                    "background": f"{('#eff6ff' if is_selected else 'white')}",
                    "borderRadius": "8px",
                    "boxShadow": f"{('0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)' if is_selected else 'none')}",
                }
        self._construct_sql()

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
        tables_to_join = tables[1:]
        for table_to_join in tables_to_join:
            join_found = False
            for existing_table in joined_tables:
                key1 = f"{existing_table}-{table_to_join}"
                key2 = f"{table_to_join}-{existing_table}"
                if key1 in self.RELATIONSHIPS:
                    condition = self.RELATIONSHIPS[key1]
                    query_parts.append(f'LEFT JOIN "{table_to_join}" ON {condition}')
                    join_found = True
                    break
                if key2 in self.RELATIONSHIPS:
                    condition = self.RELATIONSHIPS[key2]
                    query_parts.append(f'LEFT JOIN "{table_to_join}" ON {condition}')
                    join_found = True
                    break
            if not join_found:
                query_parts.append(f'CROSS JOIN "{table_to_join}"')
            joined_tables.add(table_to_join)
        self.generated_sql = " ".join(query_parts)

    @rx.event
    def clear_query(self):
        """Clear the query builder."""
        self.selected_tables = []
        self.generated_sql = ""
        self.query_results = []
        self.query_columns = []
        self.error_message = ""
        for i, n in enumerate(self.nodes):
            self.nodes[i]["style"] = {
                "border": "1px solid #777",
                "padding": "10px",
                "background": "white",
                "borderRadius": "8px",
            }

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
                self.error_message = f"Query failed: {e}"
                self.loading = False