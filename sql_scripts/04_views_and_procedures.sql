USE sales_analysis_db;

DROP VIEW IF EXISTS vw_sales_summary;
DROP VIEW IF EXISTS vw_monthly_trend;
DROP VIEW IF EXISTS vw_top_products;

CREATE VIEW vw_sales_summary AS
SELECT
    Region,
    Product_Category,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Region, Product_Category;

CREATE VIEW vw_monthly_trend AS
SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS Year_Month,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY DATE_FORMAT(Order_Date, '%Y-%m');

CREATE VIEW vw_top_products AS
SELECT
    Product_Name,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Product_Name
ORDER BY Total_Sales DESC;

DROP PROCEDURE IF EXISTS sp_get_sales_by_region;
DROP PROCEDURE IF EXISTS sp_get_sales_by_date_range;
DROP PROCEDURE IF EXISTS sp_get_customer_analysis;

DELIMITER $$

CREATE PROCEDURE sp_get_sales_by_region(IN p_region VARCHAR(20))
BEGIN
    SELECT
        Region,
        State,
        City,
        SUM(Sales_Amount) AS Total_Sales,
        SUM(Profit) AS Total_Profit,
        COUNT(DISTINCT Order_ID) AS Total_Orders
    FROM sales_data
    WHERE Region = p_region
    GROUP BY Region, State, City
    ORDER BY Total_Sales DESC;
END $$

CREATE PROCEDURE sp_get_sales_by_date_range(IN p_start DATE, IN p_end DATE)
BEGIN
    SELECT
        Order_Date,
        SUM(Sales_Amount) AS Total_Sales,
        SUM(Profit) AS Total_Profit,
        COUNT(DISTINCT Order_ID) AS Total_Orders
    FROM sales_data
    WHERE Order_Date BETWEEN p_start AND p_end
    GROUP BY Order_Date
    ORDER BY Order_Date;
END $$

CREATE PROCEDURE sp_get_customer_analysis(IN p_segment VARCHAR(30))
BEGIN
    SELECT
        Customer_Name,
        Segment,
        Customer_Type,
        SUM(Sales_Amount) AS Total_Sales,
        SUM(Profit) AS Total_Profit,
        COUNT(DISTINCT Order_ID) AS Total_Orders
    FROM sales_data
    WHERE Segment = p_segment
    GROUP BY Customer_Name, Segment, Customer_Type
    ORDER BY Total_Sales DESC;
END $$

DELIMITER ;
