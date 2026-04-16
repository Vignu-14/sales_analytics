USE sales_analysis_db;

-- 1. Overall KPIs
SELECT
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity,
    AVG(Sales_Amount) AS Avg_Order_Value
FROM sales_data;

-- 2. Sales by Region with RANK()
SELECT
    Region,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    RANK() OVER (ORDER BY SUM(Sales_Amount) DESC) AS Sales_Rank
FROM sales_data
GROUP BY Region;

-- 3. Sales by Segment
SELECT
    Segment,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Segment
ORDER BY Total_Sales DESC;

-- 4. Top 5 Products by Revenue
SELECT
    Product_Name,
    SUM(Sales_Amount) AS Revenue,
    SUM(Profit) AS Profit
FROM sales_data
GROUP BY Product_Name
ORDER BY Revenue DESC
LIMIT 5;

-- 5. Top 5 Customers by Purchase
SELECT
    Customer_Name,
    SUM(Sales_Amount) AS Revenue,
    COUNT(DISTINCT Order_ID) AS Orders_Count
FROM sales_data
GROUP BY Customer_Name
ORDER BY Revenue DESC
LIMIT 5;

-- 6. Monthly Sales Trend (DATE_FORMAT)
SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS Year_Month,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
ORDER BY Year_Month;

-- 7. Category and Sub_Category analysis
SELECT
    Product_Category,
    Sub_Category,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Product_Category, Sub_Category
ORDER BY Total_Sales DESC;

-- 8. Sales by Payment_Method
SELECT
    Payment_Method,
    SUM(Sales_Amount) AS Total_Sales,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Payment_Method
ORDER BY Total_Sales DESC;

-- 9. Sales by Sales_Channel
SELECT
    Sales_Channel,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Total_Orders
FROM sales_data
GROUP BY Sales_Channel
ORDER BY Total_Sales DESC;

-- 10. Year-over-Year growth using LAG()
WITH yearly_sales AS (
    SELECT
        YEAR(Order_Date) AS Sales_Year,
        SUM(Sales_Amount) AS Total_Sales
    FROM sales_data
    GROUP BY YEAR(Order_Date)
)
SELECT
    Sales_Year,
    Total_Sales,
    LAG(Total_Sales) OVER (ORDER BY Sales_Year) AS Previous_Year_Sales,
    ROUND(
        ((Total_Sales - LAG(Total_Sales) OVER (ORDER BY Sales_Year))
        / NULLIF(LAG(Total_Sales) OVER (ORDER BY Sales_Year), 0)) * 100,
        2
    ) AS YoY_Growth_Percent
FROM yearly_sales
ORDER BY Sales_Year;

-- 11. Loss-making products (Profit < 0)
SELECT
    Product_Name,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY Product_Name
HAVING SUM(Profit) < 0
ORDER BY Total_Profit ASC;

-- 12. Running Total by Month (window function)
WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(Order_Date, '%Y-%m') AS Year_Month,
        SUM(Sales_Amount) AS Total_Sales
    FROM sales_data
    GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
)
SELECT
    Year_Month,
    Total_Sales,
    SUM(Total_Sales) OVER (ORDER BY Year_Month) AS Running_Total
FROM monthly_sales
ORDER BY Year_Month;

-- 13. Customer Segmentation CASE
SELECT
    Customer_Name,
    SUM(Sales_Amount) AS Lifetime_Value,
    CASE
        WHEN SUM(Sales_Amount) > 10000 THEN 'High'
        WHEN SUM(Sales_Amount) BETWEEN 5000 AND 10000 THEN 'Medium'
        ELSE 'Low'
    END AS Customer_Segment
FROM sales_data
GROUP BY Customer_Name
ORDER BY Lifetime_Value DESC;

-- 14. Ship Mode analysis
SELECT
    Ship_Mode,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    AVG(DATEDIFF(Ship_Date, Order_Date)) AS Avg_Shipping_Days,
    SUM(Sales_Amount) AS Total_Sales
FROM sales_data
GROUP BY Ship_Mode
ORDER BY Avg_Shipping_Days;

-- 15. State-wise Top 10
SELECT
    State,
    SUM(Sales_Amount) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales_data
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 10;
