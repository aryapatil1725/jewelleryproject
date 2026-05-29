-- PostgreSQL Schema for Jewellery Shop Database
-- Converted from MySQL to PostgreSQL

CREATE TABLE Customer (
    CustomerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(150),
    Address VARCHAR(255),
    Password VARCHAR(255)
);

CREATE TABLE Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(150),
    TypeID INTEGER,
    ForGender VARCHAR(20),
    Weight VARCHAR(100),
    QuantityInStock INTEGER,
    Description VARCHAR(90),
    Photo VARCHAR(70)
);

CREATE TABLE OrderMaster (
    OrderID SERIAL PRIMARY KEY,
    CustomerID VARCHAR(100),
    OrderDate VARCHAR(100),
    TotalAmount VARCHAR(100),
    LabourCharges VARCHAR(100),
    GSTAmt VARCHAR(90),
    GrandTotal INTEGER
);

CREATE TABLE OrderDetails (
    OrderDetailID SERIAL PRIMARY KEY,
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity VARCHAR(100),
    Rate VARCHAR(100),
    Subtotal VARCHAR(90)
);

CREATE TABLE JwelleryType (
    TypeID SERIAL PRIMARY KEY,
    TypeName VARCHAR(100)
);

CREATE TABLE Payment (
    PaymentID SERIAL PRIMARY KEY,
    OrderID INTEGER,
    PaymentDate VARCHAR(100),
    AmountPaid VARCHAR(100),
    PaymentMethod VARCHAR(100)
);