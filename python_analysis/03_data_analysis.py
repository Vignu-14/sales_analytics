"""Generate descriptive business analysis and export results to text."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from tabulate import tabulate
except ImportError:  # pragma: no cover - fallback for machines without tabulate installed
    tabulate = None


BASE_DIR = Path(r"C:\anil")
INPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"
OUTPUT_FILE = BASE_DIR / "analysis_results.txt"


def configure_console() -> None:
    """Enable UTF-8 console output where supported."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def format_currency(value: float) -> str:
    return f"₹{value:,.2f}"


def format_number(value: float) -> str:
    return f"{value:,.0f}"


def format_percentage(value: float) -> str:
    return f"{value:,.2f}%"


def df_to_table(
    dataframe: pd.DataFrame,
    money_columns: list[str] | None = None,
    percentage_columns: list[str] | None = None,
    integer_columns: list[str] | None = None,
) -> str:
    """Convert a dataframe to a nicely formatted text table."""
    table_frame = dataframe.copy()
    money_columns = money_columns or []
    percentage_columns = percentage_columns or []
    integer_columns = integer_columns or []

    for column in money_columns:
        if column in table_frame.columns:
            table_frame[column] = table_frame[column].astype(float).map(format_currency)

    for column in percentage_columns:
        if column in table_frame.columns:
            table_frame[column] = table_frame[column].astype(float).map(format_percentage)

    for column in integer_columns:
        if column in table_frame.columns:
            table_frame[column] = table_frame[column].astype(float).map(format_number)

    if tabulate is None:
        return table_frame.to_string(index=False)
    return tabulate(table_frame, headers="keys", tablefmt="psql", showindex=False)


def overall_kpis(dataframe: pd.DataFrame) -> pd.DataFrame:
    total_sales = dataframe["Sales_Amount"].sum()
    total_profit = dataframe["Profit"].sum()
    total_orders = dataframe["Order ID"].nunique()
    total_quantity = dataframe["Quantity"].sum()
    avg_order_value = total_sales / total_orders if total_orders else 0
    overall_margin = (total_profit / total_sales * 100) if total_sales else 0
    avg_shipping = dataframe["Shipping_Days"].mean()

    return pd.DataFrame(
        {
            "Metric": [
                "Total Sales",
                "Total Profit",
                "Total Orders",
                "Total Quantity",
                "Avg Order Value",
                "Overall Profit Margin %",
                "Unique Customers",
                "Unique Products",
                "Avg Shipping Days",
            ],
            "Value": [
                format_currency(total_sales),
                format_currency(total_profit),
                format_number(total_orders),
                format_number(total_quantity),
                format_currency(avg_order_value),
                format_percentage(overall_margin),
                format_number(dataframe["Customer ID"].nunique()),
                format_number(dataframe["Product ID"].nunique()),
                f"{avg_shipping:,.2f}",
            ],
        }
    )


def compute_discount_proxy(dataframe: pd.DataFrame) -> pd.Series:
    """Estimate discount percentage using price * quantity versus sales amount."""
    expected_sales = dataframe["Unit_Price"] * dataframe["Quantity"]
    return np.where(expected_sales > 0, ((expected_sales - dataframe["Sales_Amount"]) / expected_sales) * 100, 0)


def build_report(dataframe: pd.DataFrame) -> str:
    """Build the complete analysis report as formatted text."""
    sections: list[str] = []
    dataframe = dataframe.copy()
    dataframe["Discount_Proxy"] = compute_discount_proxy(dataframe)

    sections.append("SALES PERFORMANCE & PROFIT ANALYSIS RESULTS")
    sections.append("=" * 80)
    sections.append("")

    sections.append("1. OVERALL KPIs")
    sections.append(df_to_table(overall_kpis(dataframe)))
    sections.append("")

    segment_df = (
        dataframe.groupby("Segment", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    sections.append("2. SEGMENT ANALYSIS")
    sections.append(df_to_table(segment_df, money_columns=["Sales", "Profit"], integer_columns=["Orders"]))
    sections.append("")

    region_df = (
        dataframe.groupby("Region", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
    )
    region_df["Margin %"] = np.where(region_df["Sales"] > 0, (region_df["Profit"] / region_df["Sales"]) * 100, 0)
    region_df = region_df.sort_values("Sales", ascending=False)
    best_region = region_df.iloc[0]
    worst_region = region_df.iloc[-1]
    sections.append("3. REGIONAL ANALYSIS")
    sections.append(
        df_to_table(
            region_df,
            money_columns=["Sales", "Profit"],
            percentage_columns=["Margin %"],
            integer_columns=["Orders"],
        )
    )
    sections.append(f"Best Region by Sales : {best_region['Region']} ({format_currency(best_region['Sales'])})")
    sections.append(f"Worst Region by Sales: {worst_region['Region']} ({format_currency(worst_region['Sales'])})")
    sections.append("")

    category_df = (
        dataframe.groupby("Product_Category", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"), Avg_Discount=("Discount_Proxy", "mean"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    subcategory_df = (
        dataframe.groupby(["Product_Category", "Sub_Category"], dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"), Avg_Discount=("Discount_Proxy", "mean"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    sections.append("4. CATEGORY ANALYSIS")
    sections.append("Product Category Summary")
    sections.append(
        df_to_table(
            category_df,
            money_columns=["Sales", "Profit"],
            percentage_columns=["Avg_Discount"],
            integer_columns=["Orders"],
        )
    )
    sections.append("")
    sections.append("Top Sub-Category Summary")
    sections.append(
        df_to_table(
            subcategory_df.head(15),
            money_columns=["Sales", "Profit"],
            percentage_columns=["Avg_Discount"],
            integer_columns=["Orders"],
        )
    )
    sections.append("")

    product_sales_df = (
        dataframe.groupby("Product Name", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )
    top_products_df = product_sales_df.sort_values("Sales", ascending=False).head(10)
    bottom_products_df = product_sales_df.sort_values("Profit", ascending=True).head(10)
    top_customers_df = (
        dataframe.groupby("Customer Name", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    top_states_df = (
        dataframe.groupby("State", dropna=False)
        .agg(Revenue=("Sales_Amount", "sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(5)
    )
    top_cities_df = (
        dataframe.groupby("City", dropna=False)
        .agg(Revenue=("Sales_Amount", "sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(5)
    )
    sections.append("5. TOP PERFORMERS")
    sections.append("Top 10 Products by Sales")
    sections.append(df_to_table(top_products_df, money_columns=["Sales", "Profit"]))
    sections.append("")
    sections.append("Top 10 Customers by Sales")
    sections.append(df_to_table(top_customers_df, money_columns=["Sales"], integer_columns=["Orders"]))
    sections.append("")
    sections.append("Top 5 States by Revenue")
    sections.append(df_to_table(top_states_df, money_columns=["Revenue"]))
    sections.append("")
    sections.append("Top 5 Cities by Revenue")
    sections.append(df_to_table(top_cities_df, money_columns=["Revenue"]))
    sections.append("")
    sections.append("Bottom 10 Products by Profit")
    sections.append(df_to_table(bottom_products_df, money_columns=["Sales", "Profit"]))
    sections.append("")

    monthly_df = (
        dataframe.groupby("Year_Month", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Year_Month")
    )
    quarterly_df = (
        dataframe.groupby(["Year", "Quarter"], dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values(["Year", "Quarter"])
    )
    yearly_df = (
        dataframe.groupby("Year", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Year")
    )
    yearly_df["YoY Growth %"] = yearly_df["Sales"].pct_change().mul(100).fillna(0)
    best_month = monthly_df.loc[monthly_df["Sales"].idxmax()]
    worst_month = monthly_df.loc[monthly_df["Sales"].idxmin()]
    sections.append("6. TIME ANALYSIS")
    sections.append("Monthly Sales Trend")
    sections.append(df_to_table(monthly_df, money_columns=["Sales", "Profit"]))
    sections.append("")
    sections.append("Quarterly Comparison")
    sections.append(df_to_table(quarterly_df, money_columns=["Sales", "Profit"]))
    sections.append("")
    sections.append("Year-over-Year Growth")
    sections.append(df_to_table(yearly_df, money_columns=["Sales", "Profit"], percentage_columns=["YoY Growth %"]))
    sections.append(f"Best Month by Sales : {best_month['Year_Month']} ({format_currency(best_month['Sales'])})")
    sections.append(f"Worst Month by Sales: {worst_month['Year_Month']} ({format_currency(worst_month['Sales'])})")
    sections.append("")

    channel_df = (
        dataframe.groupby("Sales_Channel", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    payment_df = (
        dataframe.groupby("Payment_Method", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    customer_type_df = (
        dataframe.groupby("Customer_Type", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    sections.append("7. CHANNEL ANALYSIS")
    sections.append("Sales Channel")
    sections.append(df_to_table(channel_df, money_columns=["Sales"], integer_columns=["Orders"]))
    sections.append("")
    sections.append("Payment Method Breakdown")
    sections.append(df_to_table(payment_df, money_columns=["Sales"], integer_columns=["Orders"]))
    sections.append("")
    sections.append("Customer Type Analysis")
    sections.append(df_to_table(customer_type_df, money_columns=["Sales", "Profit"], integer_columns=["Orders"]))
    sections.append("")

    shipping_df = (
        dataframe.groupby("Ship Mode", dropna=False)
        .agg(Sales=("Sales_Amount", "sum"), Orders=("Order ID", "nunique"), Avg_Shipping_Days=("Shipping_Days", "mean"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    sections.append("8. SHIPPING ANALYSIS")
    sections.append(df_to_table(shipping_df, money_columns=["Sales"], integer_columns=["Orders"]))
    sections.append("")

    margin_distribution_df = (
        dataframe["Margin_Category"]
        .value_counts(dropna=False)
        .rename_axis("Margin_Category")
        .reset_index(name="Count")
    )
    margin_by_category_df = (
        dataframe.groupby("Product_Category", dropna=False)
        .agg(Avg_Margin=("Profit_Margin", "mean"))
        .reset_index()
        .sort_values("Avg_Margin", ascending=False)
    )
    margin_by_region_df = (
        dataframe.groupby("Region", dropna=False)
        .agg(Avg_Margin=("Profit_Margin", "mean"))
        .reset_index()
        .sort_values("Avg_Margin", ascending=False)
    )
    margin_by_segment_df = (
        dataframe.groupby("Segment", dropna=False)
        .agg(Avg_Margin=("Profit_Margin", "mean"))
        .reset_index()
        .sort_values("Avg_Margin", ascending=False)
    )
    sections.append("9. PROFIT MARGIN")
    sections.append("Margin Category Distribution")
    sections.append(df_to_table(margin_distribution_df, integer_columns=["Count"]))
    sections.append("")
    sections.append("Average Margin by Category")
    sections.append(df_to_table(margin_by_category_df, percentage_columns=["Avg_Margin"]))
    sections.append("")
    sections.append("Average Margin by Region")
    sections.append(df_to_table(margin_by_region_df, percentage_columns=["Avg_Margin"]))
    sections.append("")
    sections.append("Average Margin by Segment")
    sections.append(df_to_table(margin_by_segment_df, percentage_columns=["Avg_Margin"]))

    return "\n".join(sections)


def main() -> None:
    """Entry point for descriptive analysis."""
    try:
        configure_console()
        print(f"Reading cleaned dataset: {INPUT_FILE}")
        dataframe = pd.read_csv(INPUT_FILE, parse_dates=["Order Date", "Ship Date"])

        report_text = build_report(dataframe)
        OUTPUT_FILE.write_text(report_text, encoding="utf-8")

        print(report_text)
        print(f"\nAnalysis report saved to: {OUTPUT_FILE}")
        print("\nStep 03 completed successfully.")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error in 03_data_analysis.py: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
