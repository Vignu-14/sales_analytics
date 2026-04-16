# Power BI Dashboard Guide

## 1. Import the Data
- Open Power BI Desktop.
- Select `Get Data > Text/CSV`.
- Import `C:\anil\cleaned_sales_data.csv`.
- In Power Query, verify these data types:
  - `Order Date`, `Ship Date` as Date
  - `Sales_Amount`, `Unit_Price`, `Unit_Cost`, `Profit`, `Profit_Margin`, `Shipping_Days` as Decimal Number
  - `Quantity`, `Month`, `Year` as Whole Number
  - All identifier and category fields as Text
- Click `Close & Apply`.

## 2. Create the Date Table
- Go to `Modeling > New Table`.
- Paste the DateTable DAX from `powerbi_measures.txt`.
- Mark the table as the official date table using the `Date` column.
- Create a relationship:
  - `DateTable[Date]` -> `Sales[Order Date]`

## 3. Create Measures
- Open `C:\anil\powerbi\powerbi_measures.txt`.
- Add each DAX measure in the `Sales` table.
- Recommended measure groups:
  - Core KPIs
  - Time Intelligence
  - Margin and Shipping
  - Ranking and Forecast Support

## 4. Apply the Theme
- Go to `View > Themes > Browse for themes`.
- Load `C:\anil\powerbi\powerbi_theme.json`.
- Confirm the visuals use the navy, gold, green, red, and blue palette.

## 5. Build Page 1: Executive Dashboard
- Page title: `Sales Performance Dashboard`
- Visual layout:
  - Top row: cards for Total Sales, Total Profit, Total Orders, Profit Margin %, Avg Order Value, Total Customers
  - Left middle: line chart for Monthly Sales Trend
  - Right middle: donut chart for Region Sales
  - Bottom left: clustered bar chart for Category Performance
  - Bottom right: pie chart for Segment Analysis
- Add slicers for `Region`, `Segment`, `Customer_Type`, and `Sales_Channel`

## 6. Build Page 2: Regional Analysis
- Visual layout:
  - Map or filled map: State sales
  - Bar chart: Region sales vs profit
  - Table: City, State, Region, Sales_Amount, Profit
  - Matrix: Region > State breakdown
- Add drill-through from Region to State.

## 7. Build Page 3: Product Intelligence
- Visual layout:
  - Horizontal bar chart: Top 10 Product Name by Sales
  - Table: Bottom 10 products by Profit
  - Column chart: Sales by Product_Category
  - Column chart: Profit_Margin by Product_Category
  - Sub_Category comparison visual
- Add a search slicer for `Product Name`.

## 8. Build Page 4: Trends and Forecasting
- Visual layout:
  - Line chart: Monthly Sales Trend
  - Column chart: Yearly Sales vs Profit
  - Column chart: Quarterly Breakdown
  - Forecast line chart using Analytics pane or imported forecast data
  - KPI cards: R2, RMSE, Avg Shipping Days
- Add bookmarks:
  - `Executive View`
  - `Regional Drilldown`
  - `Forecast Focus`

## 9. Add Interactions and Formatting
- Edit interactions so slicers affect all visuals.
- Keep white visual backgrounds and light gray page background.
- Use Segoe UI for all titles and labels.
- Display currency in Indian Rupees where possible.

## 10. Publish Checklist
- Validate all filters and slicers.
- Check totals against `analysis_results.txt`.
- Export the report as PDF for academic submission if required.
