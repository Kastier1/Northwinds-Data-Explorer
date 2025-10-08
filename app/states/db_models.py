import reflex as rx
from typing import TypedDict, Optional


class Employee(TypedDict):
    EmployeeID: int
    LastName: str
    FirstName: str
    Title: str
    TitleOfCourtesy: str
    BirthDate: str | None
    HireDate: str | None
    Address: str
    City: str
    Region: str | None
    PostalCode: str
    Country: str
    HomePhone: str
    Extension: str
    Notes: str
    ReportsTo: int | None
    PhotoPath: str


class Category(TypedDict):
    CategoryID: int
    CategoryName: str
    Description: str
    Picture: bytes | None


class Customer(TypedDict):
    CustomerID: str
    CompanyName: str
    ContactName: str
    ContactTitle: str
    Address: str
    City: str
    Region: str | None
    PostalCode: str
    Country: str
    Phone: str
    Fax: str | None


class Shipper(TypedDict):
    ShipperID: int
    CompanyName: str
    Phone: str


class Supplier(TypedDict):
    SupplierID: int
    CompanyName: str
    ContactName: str
    ContactTitle: str
    Address: str
    City: str
    Region: str | None
    PostalCode: str
    Country: str
    Phone: str
    Fax: str | None
    HomePage: str | None


class Order(TypedDict):
    OrderID: int
    CustomerID: str
    EmployeeID: int
    OrderDate: str | None
    RequiredDate: str | None
    ShippedDate: str | None
    ShipVia: int
    Freight: float
    ShipName: str
    ShipAddress: str
    ShipCity: str
    ShipRegion: str | None
    ShipPostalCode: str
    ShipCountry: str


class Product(TypedDict):
    ProductID: int
    ProductName: str
    SupplierID: int
    CategoryID: int
    QuantityPerUnit: str
    UnitPrice: float
    UnitsInStock: int
    UnitsOnOrder: int
    ReorderLevel: int
    Discontinued: bool


class OrderDetail(TypedDict):
    OrderID: int
    ProductID: int
    UnitPrice: float
    Quantity: int
    Discount: float