import reflex as rx
from typing import Any, Union
from sqlalchemy import text
import logging


class QueryBuilderState(rx.State):
    """State for the SQL query builder."""

    dropped_tables: list[str] = []
    generated_sql: str = ""
    query_results: list[dict[str, Union[str, int, float, bool, bytes, None]]] = []
    query_columns: list[str] = []
    loading: bool = False
    error_message: str = ""

    @rx.event
    def add_table_to_query(self, item: dict[str, Any]):
        """Add a table to the query builder drop zone."""
        table_name = item.get("id")
        if table_name and table_name not in self.dropped_tables:
            self.dropped_tables.append(table_name)
            self._construct_sql()

    @rx.event
    def remove_table(self, table_name: str):
        """Remove a table from the query builder."""
        if table_name in self.dropped_tables:
            self.dropped_tables.remove(table_name)
            self._construct_sql()

    @rx.event
    def clear_query(self):
        """Clear the query builder."""
        self.dropped_tables = []
        self.generated_sql = ""
        self.query_results = []
        self.query_columns = []
        self.error_message = ""

    def _construct_sql(self):
        """Construct a SQL query based on selected tables."""
        if not self.dropped_tables:
            self.generated_sql = ""
            return
        tables = self.dropped_tables
        if len(tables) == 1:
            self.generated_sql = f'SELECT * FROM "{tables[0]}" LIMIT 100'
            return
        joins = {
            ("Orders", "Customers"): "Orders.CustomerID = Customers.CustomerID",
            ("Orders", "Employees"): "Orders.EmployeeID = Employees.EmployeeID",
            ("Orders", "Shippers"): "Orders.ShipVia = Shippers.ShipperID",
            ("Order Details", "Orders"): '"Order Details".OrderID = Orders.OrderID',
            (
                "Order Details",
                "Products",
            ): '"Order Details".ProductID = Products.ProductID',
            ("Products", "Categories"): "Products.CategoryID = Categories.CategoryID",
            ("Products", "Suppliers"): "Products.SupplierID = Suppliers.SupplierID",
            (
                "EmployeeTerritories",
                "Employees",
            ): "EmployeeTerritories.EmployeeID = Employees.EmployeeID",
            (
                "EmployeeTerritories",
                "Territories",
            ): "EmployeeTerritories.TerritoryID = Territories.TerritoryID",
        }
        query_parts = [f'SELECT * FROM "{tables[0]}"']
        joined_tables = {tables[0]}
        for table_to_join in tables[1:]:
            join_found = False
            for existing_table in joined_tables:
                if (existing_table, table_to_join) in joins:
                    condition = joins[existing_table, table_to_join]
                    query_parts.append(f'LEFT JOIN "{table_to_join}" ON {condition}')
                    join_found = True
                    break
                if (table_to_join, existing_table) in joins:
                    condition = joins[table_to_join, existing_table]
                    query_parts.append(f'LEFT JOIN "{table_to_join}" ON {condition}')
                    join_found = True
                    break
            if join_found:
                joined_tables.add(table_to_join)
            else:
                query_parts.append(f'CROSS JOIN "{table_to_join}"')
                joined_tables.add(table_to_join)
        query_parts.append("LIMIT 100")
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
                self.error_message = f"Query failed: {e}"
                self.loading = False