
CREATE TABLE authors (
	au_id VARCHAR(11) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_lname VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_fname VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	phone CHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('UNKNOWN'), 
	address VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	zip CHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	contract BIT NOT NULL, 
	CONSTRAINT [UPKCL_auidind] PRIMARY KEY CLUSTERED (au_id)
)


CREATE NONCLUSTERED INDEX aunmind ON authors (au_lname, au_fname)

CREATE TABLE [Categories] (
	[CategoryID] INTEGER NOT NULL IDENTITY(1,1), 
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Description] NTEXT(8) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Picture] IMAGE NULL, 
	CONSTRAINT [PK_Categories] PRIMARY KEY CLUSTERED ([CategoryID])
)


CREATE NONCLUSTERED INDEX [CategoryName] ON [Categories] ([CategoryName])

CREATE TABLE [CustomerDemographics] (
	[CustomerTypeID] NCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[CustomerDesc] NTEXT(8) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_CustomerDemographics] PRIMARY KEY NONCLUSTERED ([CustomerTypeID])
)



CREATE TABLE [Customers] (
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ContactName] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ContactTitle] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Address] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Region] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[PostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Phone] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Fax] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_Customers] PRIMARY KEY CLUSTERED ([CustomerID])
)


CREATE NONCLUSTERED INDEX [PostalCode] ON [Customers] ([PostalCode])
CREATE NONCLUSTERED INDEX [CompanyName] ON [Customers] ([CompanyName])
CREATE NONCLUSTERED INDEX [Region] ON [Customers] ([Region])
CREATE NONCLUSTERED INDEX [City] ON [Customers] ([City])

CREATE TABLE stores (
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	stor_name VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	stor_address VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	zip CHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [UPK_storeid] PRIMARY KEY CLUSTERED (stor_id)
)



CREATE TABLE jobs (
	job_id SMALLINT NOT NULL IDENTITY(1,1), 
	job_desc VARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('New Position - title not formalized yet'), 
	min_lvl TINYINT NOT NULL, 
	max_lvl TINYINT NOT NULL, 
	CONSTRAINT [PK__jobs__6E32B6A5314C5C17] PRIMARY KEY CLUSTERED (job_id)
)



CREATE TABLE publishers (
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	pub_name VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	city VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	state CHAR(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	country VARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL DEFAULT ('USA'), 
	CONSTRAINT [UPKCL_pubind] PRIMARY KEY CLUSTERED (pub_id)
)



CREATE TABLE [Employees] (
	[EmployeeID] INTEGER NOT NULL IDENTITY(1,1), 
	[LastName] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[FirstName] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Title] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[TitleOfCourtesy] NVARCHAR(25) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[BirthDate] DATETIME NULL, 
	[HireDate] DATETIME NULL, 
	[Address] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Region] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[PostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[HomePhone] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Extension] NVARCHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Photo] IMAGE NULL, 
	[Notes] NTEXT(8) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ReportsTo] INTEGER NULL, 
	[PhotoPath] NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_Employees] PRIMARY KEY CLUSTERED ([EmployeeID]), 
	CONSTRAINT [FK_Employees_Employees] FOREIGN KEY([ReportsTo]) REFERENCES [Employees] ([EmployeeID])
)


CREATE NONCLUSTERED INDEX [LastName] ON [Employees] ([LastName])
CREATE NONCLUSTERED INDEX [PostalCode] ON [Employees] ([PostalCode])

CREATE TABLE [Region] (
	[RegionID] INTEGER NOT NULL, 
	[RegionDescription] NCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	CONSTRAINT [PK_Region] PRIMARY KEY NONCLUSTERED ([RegionID])
)



CREATE TABLE [Shippers] (
	[ShipperID] INTEGER NOT NULL IDENTITY(1,1), 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Phone] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_Shippers] PRIMARY KEY CLUSTERED ([ShipperID])
)



CREATE TABLE [Suppliers] (
	[SupplierID] INTEGER NOT NULL IDENTITY(1,1), 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ContactName] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ContactTitle] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Address] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Region] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[PostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Phone] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Fax] NVARCHAR(24) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[HomePage] NTEXT(8) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_Suppliers] PRIMARY KEY CLUSTERED ([SupplierID])
)


CREATE NONCLUSTERED INDEX [PostalCode] ON [Suppliers] ([PostalCode])
CREATE NONCLUSTERED INDEX [CompanyName] ON [Suppliers] ([CompanyName])

CREATE TABLE [Alphabetical list of products] (
	[ProductID] INTEGER NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[SupplierID] INTEGER NULL, 
	[CategoryID] INTEGER NULL, 
	[QuantityPerUnit] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[UnitPrice] MONEY NULL, 
	[UnitsInStock] SMALLINT NULL, 
	[UnitsOnOrder] SMALLINT NULL, 
	[ReorderLevel] SMALLINT NULL, 
	[Discontinued] BIT NOT NULL, 
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
)



CREATE TABLE [Category Sales for 1997] (
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[CategorySales] MONEY NULL
)



CREATE TABLE [Current Product List] (
	[ProductID] INTEGER NOT NULL IDENTITY, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
)



CREATE TABLE [Customer and Suppliers by City] (
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ContactName] NVARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Relationship] VARCHAR(9) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL
)



CREATE TABLE [Invoices] (
	[ShipName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipAddress] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCity] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipRegion] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipPostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCountry] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[CustomerName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Address] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Region] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[PostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Salesperson] NVARCHAR(31) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[OrderID] INTEGER NOT NULL, 
	[OrderDate] DATETIME NULL, 
	[RequiredDate] DATETIME NULL, 
	[ShippedDate] DATETIME NULL, 
	[ShipperName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductID] INTEGER NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[UnitPrice] MONEY NOT NULL, 
	[Quantity] SMALLINT NOT NULL, 
	[Discount] REAL NOT NULL, 
	[ExtendedPrice] MONEY NULL, 
	[Freight] MONEY NULL
)



CREATE TABLE [Order Details Extended] (
	[OrderID] INTEGER NOT NULL, 
	[ProductID] INTEGER NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[UnitPrice] MONEY NOT NULL, 
	[Quantity] SMALLINT NOT NULL, 
	[Discount] REAL NOT NULL, 
	[ExtendedPrice] MONEY NULL
)



CREATE TABLE [Order Subtotals] (
	[OrderID] INTEGER NOT NULL, 
	[Subtotal] MONEY NULL
)



CREATE TABLE [Orders Qry] (
	[OrderID] INTEGER NOT NULL, 
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[EmployeeID] INTEGER NULL, 
	[OrderDate] DATETIME NULL, 
	[RequiredDate] DATETIME NULL, 
	[ShippedDate] DATETIME NULL, 
	[ShipVia] INTEGER NULL, 
	[Freight] MONEY NULL, 
	[ShipName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipAddress] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCity] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipRegion] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipPostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCountry] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[Address] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Region] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[PostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
)



CREATE TABLE [Product Sales for 1997] (
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductSales] MONEY NULL
)



CREATE TABLE [Products Above Average Price] (
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[UnitPrice] MONEY NULL
)



CREATE TABLE [Products by Category] (
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[QuantityPerUnit] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[UnitsInStock] SMALLINT NULL, 
	[Discontinued] BIT NOT NULL
)



CREATE TABLE [Quarterly Orders] (
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[City] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[Country] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
)



CREATE TABLE [Sales by Category] (
	[CategoryID] INTEGER NOT NULL, 
	[CategoryName] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ProductSales] MONEY NULL
)



CREATE TABLE [Sales Totals by Amount] (
	[SaleAmount] MONEY NULL, 
	[OrderID] INTEGER NOT NULL, 
	[CompanyName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[ShippedDate] DATETIME NULL
)



CREATE TABLE [Summary of Sales by Quarter] (
	[ShippedDate] DATETIME NULL, 
	[OrderID] INTEGER NOT NULL, 
	[Subtotal] MONEY NULL
)



CREATE TABLE [Summary of Sales by Year] (
	[ShippedDate] DATETIME NULL, 
	[OrderID] INTEGER NOT NULL, 
	[Subtotal] MONEY NULL
)



CREATE TABLE titleview (
	title VARCHAR(80) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_ord TINYINT NULL, 
	au_lname VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	price MONEY NULL, 
	ytd_sales INTEGER NULL, 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
)



CREATE TABLE [CustomerCustomerDemo] (
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[CustomerTypeID] NCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	CONSTRAINT [PK_CustomerCustomerDemo] PRIMARY KEY NONCLUSTERED ([CustomerID], [CustomerTypeID]), 
	CONSTRAINT [FK_CustomerCustomerDemo] FOREIGN KEY([CustomerTypeID]) REFERENCES [CustomerDemographics] ([CustomerTypeID]), 
	CONSTRAINT [FK_CustomerCustomerDemo_Customers] FOREIGN KEY([CustomerID]) REFERENCES [Customers] ([CustomerID])
)



CREATE TABLE discounts (
	discounttype VARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	lowqty SMALLINT NULL, 
	highqty SMALLINT NULL, 
	discount DECIMAL(4, 2) NOT NULL, 
	CONSTRAINT [FK__discounts__stor___07C12930] FOREIGN KEY(stor_id) REFERENCES stores (stor_id)
)



CREATE TABLE employee (
	emp_id VARCHAR(9) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	fname VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	minit CHAR(1) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	lname VARCHAR(30) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	job_id SMALLINT NOT NULL DEFAULT ((1)), 
	job_lvl TINYINT NULL DEFAULT ((10)), 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('9952'), 
	hire_date DATETIME NOT NULL DEFAULT (getdate()), 
	CONSTRAINT [PK_emp_id] PRIMARY KEY NONCLUSTERED (emp_id), 
	CONSTRAINT [FK__employee__job_id__14270015] FOREIGN KEY(job_id) REFERENCES jobs (job_id), 
	CONSTRAINT [FK__employee__pub_id__17036CC0] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)


CREATE CLUSTERED INDEX employee_ind ON employee (fname, minit, lname)

CREATE TABLE [Territories] (
	[TerritoryID] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[TerritoryDescription] NCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[RegionID] INTEGER NOT NULL, 
	CONSTRAINT [PK_Territories] PRIMARY KEY NONCLUSTERED ([TerritoryID]), 
	CONSTRAINT [FK_Territories_Region] FOREIGN KEY([RegionID]) REFERENCES [Region] ([RegionID])
)



CREATE TABLE [Orders] (
	[OrderID] INTEGER NOT NULL IDENTITY(1,1), 
	[CustomerID] NCHAR(5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[EmployeeID] INTEGER NULL, 
	[OrderDate] DATETIME NULL, 
	[RequiredDate] DATETIME NULL, 
	[ShippedDate] DATETIME NULL, 
	[ShipVia] INTEGER NULL, 
	[Freight] MONEY NULL DEFAULT ((0)), 
	[ShipName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipAddress] NVARCHAR(60) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCity] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipRegion] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipPostalCode] NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[ShipCountry] NVARCHAR(15) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [PK_Orders] PRIMARY KEY CLUSTERED ([OrderID]), 
	CONSTRAINT [FK_Orders_Customers] FOREIGN KEY([CustomerID]) REFERENCES [Customers] ([CustomerID]), 
	CONSTRAINT [FK_Orders_Employees] FOREIGN KEY([EmployeeID]) REFERENCES [Employees] ([EmployeeID]), 
	CONSTRAINT [FK_Orders_Shippers] FOREIGN KEY([ShipVia]) REFERENCES [Shippers] ([ShipperID])
)


CREATE NONCLUSTERED INDEX [EmployeesOrders] ON [Orders] ([EmployeeID])
CREATE NONCLUSTERED INDEX [CustomerID] ON [Orders] ([CustomerID])
CREATE NONCLUSTERED INDEX [CustomersOrders] ON [Orders] ([CustomerID])
CREATE NONCLUSTERED INDEX [ShippersOrders] ON [Orders] ([ShipVia])
CREATE NONCLUSTERED INDEX [ShipPostalCode] ON [Orders] ([ShipPostalCode])
CREATE NONCLUSTERED INDEX [EmployeeID] ON [Orders] ([EmployeeID])
CREATE NONCLUSTERED INDEX [OrderDate] ON [Orders] ([OrderDate])
CREATE NONCLUSTERED INDEX [ShippedDate] ON [Orders] ([ShippedDate])

CREATE TABLE [Products] (
	[ProductID] INTEGER NOT NULL IDENTITY(1,1), 
	[ProductName] NVARCHAR(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	[SupplierID] INTEGER NULL, 
	[CategoryID] INTEGER NULL, 
	[QuantityPerUnit] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	[UnitPrice] MONEY NULL DEFAULT ((0)), 
	[UnitsInStock] SMALLINT NULL DEFAULT ((0)), 
	[UnitsOnOrder] SMALLINT NULL DEFAULT ((0)), 
	[ReorderLevel] SMALLINT NULL DEFAULT ((0)), 
	[Discontinued] BIT NOT NULL DEFAULT ((0)), 
	CONSTRAINT [PK_Products] PRIMARY KEY CLUSTERED ([ProductID]), 
	CONSTRAINT [FK_Products_Categories] FOREIGN KEY([CategoryID]) REFERENCES [Categories] ([CategoryID]), 
	CONSTRAINT [FK_Products_Suppliers] FOREIGN KEY([SupplierID]) REFERENCES [Suppliers] ([SupplierID])
)


CREATE NONCLUSTERED INDEX [SupplierID] ON [Products] ([SupplierID])
CREATE NONCLUSTERED INDEX [CategoryID] ON [Products] ([CategoryID])
CREATE NONCLUSTERED INDEX [SuppliersProducts] ON [Products] ([SupplierID])
CREATE NONCLUSTERED INDEX [CategoriesProducts] ON [Products] ([CategoryID])
CREATE NONCLUSTERED INDEX [ProductName] ON [Products] ([ProductName])

CREATE TABLE pub_info (
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	logo IMAGE NULL, 
	pr_info TEXT(16) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	CONSTRAINT [UPKCL_pubinfo] PRIMARY KEY CLUSTERED (pub_id), 
	CONSTRAINT [FK__pub_info__pub_id__0F624AF8] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)



CREATE TABLE titles (
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title VARCHAR(80) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	type CHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL DEFAULT ('UNDECIDED'), 
	pub_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	price MONEY NULL, 
	advance MONEY NULL, 
	royalty INTEGER NULL, 
	ytd_sales INTEGER NULL, 
	notes VARCHAR(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, 
	pubdate DATETIME NOT NULL DEFAULT (getdate()), 
	CONSTRAINT [UPKCL_titleidind] PRIMARY KEY CLUSTERED (title_id), 
	CONSTRAINT [FK__titles__pub_id__797309D9] FOREIGN KEY(pub_id) REFERENCES publishers (pub_id)
)


CREATE NONCLUSTERED INDEX titleind ON titles (title)

CREATE TABLE [EmployeeTerritories] (
	[EmployeeID] INTEGER NOT NULL, 
	[TerritoryID] NVARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	CONSTRAINT [PK_EmployeeTerritories] PRIMARY KEY NONCLUSTERED ([EmployeeID], [TerritoryID]), 
	CONSTRAINT [FK_EmployeeTerritories_Employees] FOREIGN KEY([EmployeeID]) REFERENCES [Employees] ([EmployeeID]), 
	CONSTRAINT [FK_EmployeeTerritories_Territories] FOREIGN KEY([TerritoryID]) REFERENCES [Territories] ([TerritoryID])
)



CREATE TABLE [Order Details] (
	[OrderID] INTEGER NOT NULL, 
	[ProductID] INTEGER NOT NULL, 
	[UnitPrice] MONEY NOT NULL DEFAULT ((0)), 
	[Quantity] SMALLINT NOT NULL DEFAULT ((1)), 
	[Discount] REAL NOT NULL DEFAULT ((0)), 
	CONSTRAINT [PK_Order_Details] PRIMARY KEY CLUSTERED ([OrderID], [ProductID]), 
	CONSTRAINT [FK_Order_Details_Orders] FOREIGN KEY([OrderID]) REFERENCES [Orders] ([OrderID]), 
	CONSTRAINT [FK_Order_Details_Products] FOREIGN KEY([ProductID]) REFERENCES [Products] ([ProductID])
)


CREATE NONCLUSTERED INDEX [ProductID] ON [Order Details] ([ProductID])
CREATE NONCLUSTERED INDEX [OrderID] ON [Order Details] ([OrderID])
CREATE NONCLUSTERED INDEX [ProductsOrder_Details] ON [Order Details] ([ProductID])
CREATE NONCLUSTERED INDEX [OrdersOrder_Details] ON [Order Details] ([OrderID])

CREATE TABLE roysched (
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	lorange INTEGER NULL, 
	hirange INTEGER NULL, 
	royalty INTEGER NULL, 
	CONSTRAINT [FK__roysched__title___05D8E0BE] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX titleidind ON roysched (title_id)

CREATE TABLE sales (
	stor_id CHAR(4) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	ord_num VARCHAR(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	ord_date DATETIME NOT NULL, 
	qty SMALLINT NOT NULL, 
	payterms VARCHAR(12) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	CONSTRAINT [UPKCL_sales] PRIMARY KEY CLUSTERED (stor_id, ord_num, title_id), 
	CONSTRAINT [FK__sales__stor_id__02FC7413] FOREIGN KEY(stor_id) REFERENCES stores (stor_id), 
	CONSTRAINT [FK__sales__title_id__03F0984C] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX titleidind ON sales (title_id)

CREATE TABLE titleauthor (
	au_id VARCHAR(11) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	title_id VARCHAR(6) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, 
	au_ord TINYINT NULL, 
	royaltyper INTEGER NULL, 
	CONSTRAINT [UPKCL_taind] PRIMARY KEY CLUSTERED (au_id, title_id), 
	CONSTRAINT [FK__titleauth__au_id__7D439ABD] FOREIGN KEY(au_id) REFERENCES authors (au_id), 
	CONSTRAINT [FK__titleauth__title__7E37BEF6] FOREIGN KEY(title_id) REFERENCES titles (title_id)
)


CREATE NONCLUSTERED INDEX auidind ON titleauthor (au_id)
CREATE NONCLUSTERED INDEX titleidind ON titleauthor (title_id)
