import reflex as rx
from typing import Union
from sqlalchemy import text
from .db_models import (
    Employee,
    Category,
    Customer,
    Shipper,
    Supplier,
    Order,
    Product,
    OrderDetail,
)
from .base_state import BaseState


class DataTableState(rx.State):
    """State for the data table."""

    table_data: list[dict[str, Union[str, int, float, bool, bytes, None]]] = []
    search_query: str = ""
    current_page: int = 1
    items_per_page: int = 10
    total_items: int = 0
    loading: bool = False
    TABLE_MODEL_MAP = {
        "Employees": Employee,
        "Categories": Category,
        "Customers": Customer,
        "Shippers": Shipper,
        "Suppliers": Supplier,
        "Orders": Order,
        "Products": Product,
        "Order Details": OrderDetail,
    }

    @rx.var
    def total_pages(self) -> int:
        """The total number of pages."""
        return -(-self.total_items // self.items_per_page)

    @rx.var
    def paged_data(self) -> list[dict[str, Union[str, int, float, bool, bytes, None]]]:
        """The data for the current page."""
        return self.table_data

    @rx.var
    async def columns(self) -> list[str]:
        """The columns for the active table."""
        base_state = await self.get_state(BaseState)
        active_table = base_state.active_table
        model = self.TABLE_MODEL_MAP.get(active_table)
        if model:
            return list(model.__annotations__.keys())
        return []

    async def _get_search_columns(self) -> list[str]:
        """Returns the columns to search by for the active table."""
        base_state = await self.get_state(BaseState)
        table_name = base_state.active_table
        searchable_columns = {
            "Employees": ["FirstName", "LastName", "Title", "City", "Country"],
            "Products": ["ProductName", "QuantityPerUnit"],
            "Orders": ["ShipName", "ShipCity", "ShipCountry"],
            "Customers": ["CompanyName", "ContactName", "City", "Country"],
            "Suppliers": ["CompanyName", "ContactName", "City", "Country"],
            "Categories": ["CategoryName", "Description"],
            "Shippers": ["CompanyName"],
            "Order Details": ["OrderID", "ProductID"],
        }
        return searchable_columns.get(table_name, [])

    @rx.event(background=True)
    async def fetch_data(self):
        """Fetch data for the active table."""
        async with self:
            self.loading = True
            base_state = await self.get_state(BaseState)
            table_name = base_state.active_table
            offset = (self.current_page - 1) * self.items_per_page
            search_cols = await self._get_search_columns()
        search_clause = ""
        if self.search_query and search_cols:
            search_conditions = [
                f"CAST({col} AS NVARCHAR(MAX)) LIKE '%{self.search_query}%'"
                for col in search_cols
            ]
            search_clause = "WHERE " + " OR ".join(search_conditions)
        async with rx.asession() as session:
            count_query = text(f'SELECT COUNT(*) FROM "{table_name}" {search_clause}')
            total_result = await session.execute(count_query)
            total_items = total_result.scalar_one()
            query = text(
                f'\n                SELECT * FROM "{table_name}"\n                {search_clause}\n                ORDER BY 1\n                OFFSET {offset} ROWS\n                FETCH NEXT {self.items_per_page} ROWS ONLY\n            '
            )
            result = await session.execute(query)
            rows = result.mappings().all()
            async with self:
                self.total_items = total_items
                self.table_data = [dict(row) for row in rows]
                self.loading = False

    @rx.event
    async def set_active_table_and_fetch(self, table: str):
        """Set the active table and fetch data."""
        base_state = await self.get_state(BaseState)
        base_state.active_table = table
        self.current_page = 1
        self.search_query = ""
        return DataTableState.fetch_data

    @rx.event
    def set_search_query(self, query: str):
        """Set the search query and fetch data."""
        self.search_query = query
        self.current_page = 1
        return DataTableState.fetch_data

    @rx.event
    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            return DataTableState.fetch_data

    @rx.event
    def prev_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            return DataTableState.fetch_data