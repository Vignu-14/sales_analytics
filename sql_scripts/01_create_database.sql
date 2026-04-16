CREATE DATABASE IF NOT EXISTS sales_analysis_db;
USE sales_analysis_db;

DROP TABLE IF EXISTS sales_data;

CREATE TABLE sales_data (
    Row_ID INT NOT NULL,
    Order_ID VARCHAR(30) NOT NULL,
    Order_Date DATE,
    Ship_Date DATE,
    Ship_Mode VARCHAR(30),
    Customer_ID VARCHAR(20),
    Customer_Name VARCHAR(100),
    Segment VARCHAR(30),
    Country VARCHAR(50),
    City VARCHAR(50),
    State VARCHAR(50),
    Postal_Code VARCHAR(20),
    Region VARCHAR(20),
    Product_ID VARCHAR(30),
    Product_Category VARCHAR(50),
    Sub_Category VARCHAR(50),
    Product_Name VARCHAR(200),
    Sales_Amount DECIMAL(12,2),
    Unit_Price DECIMAL(12,2),
    Unit_Cost DECIMAL(12,2),
    Sales_Channel VARCHAR(30),
    Payment_Method VARCHAR(30),
    Customer_Type VARCHAR(30),
    Quantity INT,
    Profit DECIMAL(12,2),
    PRIMARY KEY (Row_ID),
    INDEX idx_order_date (Order_Date),
    INDEX idx_region (Region),
    INDEX idx_product_category (Product_Category),
    INDEX idx_customer_id (Customer_ID),
    INDEX idx_state (State)
);
