# Sales Performance & Profit Analysis System

## 1. Title Page

**Project Title:** Sales Performance & Profit Analysis System  
**Student Name:** ____________________  
**Course:** Bachelor of Computer Applications (BCA)  
**Academic Session:** 2024-25  
**Institution:** ____________________  

---

## 2. Abstract

Sales data is one of the most valuable assets for retail and e-commerce organizations because it captures customer behavior, product demand, regional performance, pricing efficiency, and profitability trends. This project presents a complete Sales Performance & Profit Analysis System built using Python, MySQL, Excel, Power BI, and a browser-based dashboard developed with HTML, CSS, JavaScript, and Chart.js. The system reads a real sales dataset stored in `C:\anil`, cleans and enriches it, performs descriptive analysis, generates visualizations, forecasts future monthly sales using linear regression, and publishes the results through multiple reporting layers.

The Python workflow handles data loading, missing value treatment, type conversion, duplicate order removal, derived metric creation, analysis, chart generation, and Excel export. SQL scripts provide a relational schema, sample data inserts, analytical queries, views, and procedures for database-level reporting. The frontend dashboard converts analytical outputs into an interactive and responsive visual interface. In addition, the project includes guidance for creating Excel and Power BI dashboards, enabling the same dataset to be explored by technical and non-technical users.

The final solution demonstrates how sales analytics can support strategic decision-making by identifying strong regions, profitable product groups, customer patterns, channel performance, and future trends. It is suitable as a BCA final-year project because it combines programming, databases, reporting, and business intelligence into one integrated system.

---

## 3. Introduction

Modern businesses generate a large amount of transactional data every day. In both retail stores and e-commerce platforms, this data includes order details, customer information, product categories, sales amount, pricing, shipping details, and profit values. Raw transactional data alone does not help managers unless it is cleaned, organized, analyzed, and presented in a meaningful format.

The objective of sales analytics is to transform raw records into actionable insights. By studying trends over time, comparing regions, evaluating product performance, and measuring profitability, organizations can optimize pricing, inventory, marketing, and logistics decisions. This project focuses on a realistic retail and e-commerce business context where management needs a unified system to track business performance from multiple perspectives.

### Problem Statement

The organization has a sales dataset, but decision-makers do not have a single integrated system to:
- clean and standardize the data,
- evaluate key performance indicators,
- compare regional and product performance,
- monitor profit and shipping behavior,
- forecast upcoming sales,
- and present results through business-friendly dashboards.

This project addresses that gap by developing a complete analytics pipeline and dashboard suite.

---

## 4. Objectives

1. To load and validate the real sales dataset from the existing project folder.
2. To clean missing values, data types, and duplicate order records.
3. To generate derived fields such as profit margin, shipping days, and time dimensions.
4. To calculate core sales KPIs for business reporting.
5. To analyze performance by segment, region, state, city, category, and sub-category.
6. To identify top-performing and loss-making products and customers.
7. To visualize analytical insights through professional charts.
8. To forecast future monthly sales using a machine learning model.
9. To export the processed data for frontend, Excel, and Power BI usage.
10. To build a complete academic project package with code, SQL, dashboards, and report documentation.

---

## 5. Tools & Technologies

| Tool / Technology | Purpose |
| --- | --- |
| Python | Data processing, automation, forecasting, export |
| MySQL | Database design, queries, views, procedures |
| Excel | Spreadsheet dashboard and manual pivot analysis |
| Power BI | Interactive business intelligence dashboard |
| Chart.js | Web-based interactive charts |
| HTML/CSS/JavaScript | Frontend dashboard development |
| Flask-style API / http.server | Local dashboard serving |

---

## 6. Methodology

This project follows the **CRISP-DM** methodology.

```text
+--------------------+
| Business Understanding |
+----------+---------+
           |
           v
+--------------------+
| Data Understanding |
+----------+---------+
           |
           v
+--------------------+
| Data Preparation   |
+----------+---------+
           |
           v
+--------------------+
| Modeling           |
+----------+---------+
           |
           v
+--------------------+
| Evaluation         |
+----------+---------+
           |
           v
+--------------------+
| Deployment         |
+--------------------+
```

### CRISP-DM Application in This Project
- Business Understanding: define sales and profit monitoring goals.
- Data Understanding: inspect CSV columns, types, ranges, and completeness.
- Data Preparation: clean data, convert dates, derive additional fields.
- Modeling: apply linear regression for forecasting.
- Evaluation: compare KPIs, trend behavior, and forecast metrics.
- Deployment: publish results to files, charts, Excel, Power BI, and frontend dashboard.

---

## 7. System Design

### Architecture Diagram

```text
 dataset.csv / sales.csv
          |
          v
+-----------------------+
| Python Data Pipeline  |
| load -> clean ->      |
| analyze -> visualize  |
+-----------+-----------+
            |
            v
+-----------------------+      +-----------------------+
| cleaned_sales_data.csv|----->| Excel / Power BI      |
+-----------+-----------+      +-----------------------+
            |
            v
+-----------------------+
| frontend/js/data.js   |
+-----------+-----------+
            |
            v
+-----------------------+      +-----------------------+
| backend/server.py     |----->| Browser Dashboard     |
+-----------------------+      +-----------------------+
```

### Simplified ER Diagram

```text
CUSTOMER (Customer_ID, Customer_Name, Segment, Customer_Type)
        |
        | places
        v
ORDER (Order_ID, Order_Date, Ship_Date, Ship_Mode, Region, State, City)
        |
        | contains
        v
PRODUCT (Product_ID, Product_Category, Sub_Category, Product_Name)
        |
        | contributes to
        v
SALES_DATA (Sales_Amount, Unit_Price, Unit_Cost, Quantity, Profit)
```

### Data Flow Diagram

```text
[CSV Dataset]
     |
     v
[Python Scripts]
     |
     +--> [Analysis Report]
     +--> [PNG Charts]
     +--> [Excel Workbook]
     +--> [Frontend JS Data]
     |
     v
[Backend Server]
     |
     v
[End User Dashboard]
```

---

## 8. Implementation

### 8.1 Python Layer
- `01_generate_or_load_dataset.py` validates the source file and creates a backup copy.
- `02_data_cleaning.py` handles missing values, duplicate order removal, numeric conversion, and derived fields.
- `03_data_analysis.py` calculates KPIs and writes formatted results to `analysis_results.txt`.
- `04_visualizations.py` generates all required charts using Matplotlib and Seaborn.
- `05_forecasting.py` performs monthly aggregation and 6-month sales forecasting.
- `06_export_json_for_frontend.py` creates `data.js` and the Excel workbook.

### 8.2 SQL Layer
- `01_create_database.sql` builds the MySQL schema.
- `02_insert_data.sql` loads 50 real rows from the source dataset.
- `03_analysis_queries.sql` contains 15 business analysis queries.
- `04_views_and_procedures.sql` creates reusable views and procedures.

### 8.3 Excel Layer
- The workbook includes `Data`, `Summary`, and `Charts_Guide` sheets.
- The data is formatted as a table with filters, frozen panes, and numeric formatting.

### 8.4 Power BI Layer
- Measures and a theme file are provided for quick report construction.
- The report is designed with four pages: Executive Dashboard, Regional Analysis, Product Intelligence, and Forecasting.

### 8.5 Frontend Layer
- The frontend uses a fixed sidebar layout and a responsive content area.
- All pages are powered by `dashboardData` generated from the cleaned dataset.
- Chart.js renders the interactive charts directly in the browser.

---

## 9. Screenshots and Visual Output Reference

The following generated visuals are part of the project:

1. `../python_analysis/output_charts/sales_trend.png` - Monthly sales line trend.
2. `../python_analysis/output_charts/profit_distribution.png` - Profit histogram with mean marker.
3. `../python_analysis/output_charts/category_performance.png` - Sales and profit by product category.
4. `../python_analysis/output_charts/subcategory_performance.png` - Top 15 sub-categories by sales.
5. `../python_analysis/output_charts/region_sales.png` - Donut chart showing regional sales mix.
6. `../python_analysis/output_charts/segment_analysis.png` - Segment-wise sales contribution.
7. `../python_analysis/output_charts/top_products.png` - Top 10 products by sales.
8. `../python_analysis/output_charts/monthly_heatmap.png` - Heatmap of sales by month and year.
9. `../python_analysis/output_charts/profit_margin_boxplot.png` - Margin spread by category.
10. `../python_analysis/output_charts/shipping_analysis.png` - Average shipping days with order count.
11. `../python_analysis/output_charts/payment_method.png` - Sales split by payment method.
12. `../python_analysis/output_charts/sales_channel.png` - Sales by sales channel.
13. `../python_analysis/output_charts/state_map.png` - Top states by sales in horizontal bar form.
14. `../python_analysis/output_charts/customer_type.png` - Sales and profit by customer type.
15. `../python_analysis/output_charts/correlation_heatmap.png` - Numeric feature correlation matrix.
16. `../python_analysis/output_charts/dashboard_summary.png` - Combined summary dashboard image.
17. `../python_analysis/output_charts/forecast.png` - Forecast chart with trend and confidence band.

---

## 10. Results & Analysis

The generated analysis highlights the commercial behavior of the business from multiple viewpoints. Based on the final processed dataset:
- Total Sales: `₹1,082,910.82`
- Total Profit: `₹216,582.16`
- Total Orders after duplicate-order cleanup: `4,922`
- Total Customers: `793`
- Average Order Value: `₹220.01`
- Average Shipping Days: `3.96`

### Key Findings
- The **West** region is the highest-performing region with `₹325,811.33` in sales, while the **South** region is the lowest among the four regions with `₹189,251.11`.
- **Technology** is the top-performing product category with `₹378,204.58` in sales, followed by **Furniture** and **Office Supplies`.
- The leading sub-categories are **Chairs**, **Phones**, **Storage**, and **Binders**, showing that both office essentials and technology products are major revenue drivers.
- **California** is the highest revenue state with `₹210,349.03`, and **New York City** is the top-performing city with `₹116,870.04`.
- The top product by sales is **Canon imageCLASS 2200 Advanced Copier** with `₹30,099.91`.
- The best sales month is **November 2018** with `₹62,608.74`, showing strong year-end demand.
- Forecasting projects the next 6 months in the range of roughly `₹34,888.93` to `₹37,404.91`, with an `R²` score of `0.3025` and `RMSE` of `₹10,585.62`.

### Business Recommendations
- Focus marketing and inventory planning on the **West region**, **California**, and the best-performing product families in **Technology** and **Furniture**.
- Investigate products with very low profit contribution, even when sales volume exists, because these items reduce margin efficiency.
- Monitor **Standard Class** shipping closely because it handles the highest order volume and has the longest average delivery time.
- Use customer and channel segmentation to personalize promotions for both **new** and **returning** customers.
- Use the forecast range instead of a single-point target while planning inventory, staffing, and sales goals for upcoming months.

---

## 11. Conclusion

The Sales Performance & Profit Analysis System successfully converts raw transactional data into meaningful business intelligence. The project demonstrates the practical use of Python for ETL and analytics, SQL for structured reporting, Excel and Power BI for decision support, and web technologies for a user-friendly dashboard. As a final-year BCA project, it shows both technical depth and business relevance by unifying analysis, visualization, forecasting, and multi-platform reporting into a single end-to-end system.

---

## 12. Future Scope

1. Add advanced machine learning forecasting models such as ARIMA or Prophet.
2. Integrate real-time streaming sales data.
3. Connect the project to a live MySQL or cloud database.
4. Build role-based authentication for the dashboard.
5. Add customer lifetime value prediction.
6. Add inventory and stock optimization analysis.
7. Publish the solution to a cloud platform.
8. Create a mobile-friendly companion app.
9. Include anomaly detection for fraud or unusual sales dips.
10. Add recommendation systems for cross-sell and upsell analysis.

---

## 13. References

1. Han, J., Kamber, M., and Pei, J. *Data Mining: Concepts and Techniques*. Morgan Kaufmann.
2. McKinney, W. *Python for Data Analysis*. O'Reilly Media.
3. Scikit-learn Documentation. https://scikit-learn.org/
4. Pandas Documentation. https://pandas.pydata.org/
5. Matplotlib Documentation. https://matplotlib.org/
6. Seaborn Documentation. https://seaborn.pydata.org/
7. MySQL 8.0 Reference Manual. https://dev.mysql.com/doc/
8. Microsoft Power BI Documentation. https://learn.microsoft.com/power-bi/
9. OpenPyXL Documentation. https://openpyxl.readthedocs.io/
10. Chart.js Documentation. https://www.chartjs.org/docs/
