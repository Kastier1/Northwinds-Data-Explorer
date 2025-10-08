import reflex as rx


class BaseState(rx.State):
    """The base state for the app."""

    tables: list[str] = [
        "Employees",
        "Categories",
        "Customers",
        "Shippers",
        "Suppliers",
        "Orders",
        "Products",
        "Order Details",
    ]
    active_table: str = "Employees"
    is_sidebar_open: bool = True

    @rx.event
    def set_active_table(self, table: str):
        """Set the active table."""
        self.active_table = table

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar."""
        self.is_sidebar_open = not self.is_sidebar_open