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
    async def column_defs(self) -> list[dict[str, str]]:
        """The column definitions for the active table."""
        base_state = await self.get_state(BaseState)
        active_table = base_state.active_table
        model = self.TABLE_MODEL_MAP.get(active_table)
        if model:
            cols = list(model.__annotations__.keys())
            return [
                {
                    "field": col,
                    "headerName": col,
                    "sortable": True,
                    "filter": True,
                    "resizable": True,
                }
                for col in cols
            ]
        return []

    @rx.event(background=True)
    async def fetch_data(self):
        """Fetch data for the active table."""
        async with self:
            self.loading = True
            base_state = await self.get_state(BaseState)
            table_name = base_state.active_table
            if table_name not in self.TABLE_MODEL_MAP:
                base_state.active_table = "Employees"
                table_name = "Employees"
        async with rx.asession() as session:
            query = text(f'SELECT * FROM "{table_name}"')
            result = await session.execute(query)
            rows = result.mappings().all()
            async with self:
                self.table_data = [dict(row) for row in rows]
                self.loading = False

    @rx.event
    async def set_active_table_and_fetch(self, table: str):
        """Set the active table and fetch data."""
        base_state = await self.get_state(BaseState)
        base_state.active_table = table
        self.search_query = ""
        return DataTableState.fetch_data

    @rx.event
    def set_search_query(self, query: str):
        """Set the search query for the grid."""
        self.search_query = query