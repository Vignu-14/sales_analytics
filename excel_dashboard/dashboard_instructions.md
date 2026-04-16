# Excel Dashboard Guide

## 1. Open the Workbook
- Open `C:\anil\excel_dashboard\Sales_Dashboard.xlsx`.
- Verify that the `Data`, `Summary`, and `Charts_Guide` sheets are present.
- If the file has not been generated yet, run `python C:\anil\run_all.py`.

## 2. Review the Data Sheet
- Go to the `Data` sheet.
- Confirm the table contains the cleaned dataset with filters enabled.
- Keep the first row frozen for easier scrolling.
- Check that currency and numeric columns already use comma-formatted values.

## 3. Create Pivot Tables
- Insert a Pivot Table from the `CleanedSalesData` table.
- Place each Pivot Table on a new worksheet or in a dashboard workspace sheet.
- Recommended Pivot Tables:
  - Region Pivot: `Region` in Rows, `Sales_Amount` and `Profit` in Values.
  - Category Pivot: `Product_Category` in Rows, `Sales_Amount` and `Profit` in Values.
  - Monthly Pivot: `Order Date` in Rows, group by Years and Months, `Sales_Amount` in Values.
  - Top Products Pivot: `Product Name` in Rows, `Sales_Amount` in Values, sort descending, filter Top 10.
  - Segment Pivot: `Segment` in Rows, `Sales_Amount` in Values.

## 4. Add KPI Cards
- Use formulas in a top summary area:
  - Total Sales: `=SUM(Data!R:R)` if `Sales_Amount` is in column `R`.
  - Total Profit: `=SUM(Data!Y:Y)` if `Profit` is in column `Y`.
  - Total Orders: `=COUNTA(UNIQUE(Data!B:B))-1`
  - Avg Order Value: `=TotalSalesCell/TotalOrdersCell`
  - Profit Margin: `=TotalProfitCell/TotalSalesCell`
  - Total Customers: `=COUNTA(UNIQUE(Data!F:F))-1`
- Format KPI cards with:
  - Navy fill `#1B2A4A`
  - Gold highlights `#F4B942`
  - White font for labels
  - Bold Segoe UI values

## 5. Build Charts
- Insert a clustered column chart for Region sales.
- Insert a line chart for Monthly Sales Trend.
- Insert a doughnut or pie chart for Segment analysis.
- Insert a horizontal bar chart for Top Products.
- Insert a bar chart for Product_Category sales and profit.
- Use the same color palette from the Python visuals and Power BI theme.

## 6. Add Slicers
- Insert slicers for:
  - Region
  - Segment
  - Ship Mode
  - Customer_Type
  - Payment_Method
- Align slicers in one row or one side panel for quick filtering.

## 7. Final Formatting
- Remove worksheet gridlines on the dashboard sheet.
- Keep equal spacing between charts and KPI cards.
- Use titles that match the frontend dashboard labels.
- Add a footer note:
  - `Sales Performance & Profit Analysis System | BCA Final Year Project 2024-25`

## 8. Recommended Dashboard Layout
- Top row: 6 KPI cards.
- Middle row: Monthly Sales Trend and Regional Sales.
- Next row: Category Performance and Segment Analysis.
- Bottom row: Top Products and Payment Methods.
- Side panel or footer: Slicers and notes.
