"""Create analysis charts and save them as PNG files."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter


BASE_DIR = Path(r"C:\anil")
INPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "python_analysis" / "output_charts"

PRIMARY = "#1B2A4A"
GOLD = "#F4B942"
GREEN = "#2ECC71"
RED = "#E74C3C"
BLUE = "#3498DB"
PURPLE = "#9B59B6"
ORANGE = "#E67E22"
TEAL = "#1ABC9C"


def configure_console() -> None:
    """Enable UTF-8 console output where supported."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def money_formatter(value: float, _position: float) -> str:
    return f"₹{value:,.0f}"


def use_style() -> None:
    """Apply plotting style with a safe fallback."""
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("ggplot")


def finalize_axis(axis, money_axis: str | None = None) -> None:
    """Apply shared formatting to axes."""
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.grid(alpha=0.25)
    if money_axis == "x":
        axis.xaxis.set_major_formatter(FuncFormatter(money_formatter))
    if money_axis == "y":
        axis.yaxis.set_major_formatter(FuncFormatter(money_formatter))


def save_figure(figure: plt.Figure, file_name: str) -> None:
    """Save a figure with consistent output settings."""
    output_path = OUTPUT_DIR / file_name
    figure.tight_layout()
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved chart: {output_path}")


def create_sales_trend(dataframe: pd.DataFrame) -> None:
    monthly = dataframe.groupby("Year_Month")["Sales_Amount"].sum().reset_index().sort_values("Year_Month")
    positions = np.arange(len(monthly))
    figure, axis = plt.subplots(figsize=(12, 6))
    axis.plot(positions, monthly["Sales_Amount"], color=BLUE, marker="o", linewidth=2.5)
    axis.fill_between(positions, monthly["Sales_Amount"], color=BLUE, alpha=0.15)
    axis.set_title("Monthly Sales Trend", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Month")
    axis.set_ylabel("Sales Amount")
    for x_value, y_value in zip(positions, monthly["Sales_Amount"]):
        axis.annotate(f"₹{y_value:,.0f}", xy=(x_value, y_value), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8)
    axis.set_xticks(positions)
    axis.set_xticklabels(monthly["Year_Month"], rotation=45, ha="right")
    finalize_axis(axis, money_axis="y")
    save_figure(figure, "sales_trend.png")


def create_profit_distribution(dataframe: pd.DataFrame) -> None:
    figure, axis = plt.subplots(figsize=(11, 6))
    positive_profit = dataframe.loc[dataframe["Profit"] >= 0, "Profit"]
    negative_profit = dataframe.loc[dataframe["Profit"] < 0, "Profit"]
    axis.hist(positive_profit, bins=20, color=GREEN, alpha=0.75, label="Profit ≥ 0")
    axis.hist(negative_profit, bins=20, color=RED, alpha=0.75, label="Profit < 0")
    mean_profit = dataframe["Profit"].mean()
    axis.axvline(mean_profit, color=PRIMARY, linestyle="--", linewidth=2, label=f"Mean: ₹{mean_profit:,.2f}")
    axis.set_title("Profit Distribution", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Profit")
    axis.set_ylabel("Frequency")
    axis.legend()
    finalize_axis(axis, money_axis="x")
    save_figure(figure, "profit_distribution.png")


def create_category_performance(dataframe: pd.DataFrame) -> None:
    category = dataframe.groupby("Product_Category")[["Sales_Amount", "Profit"]].sum().sort_values("Sales_Amount")
    figure, axis = plt.subplots(figsize=(11, 6))
    positions = np.arange(len(category.index))
    bar_height = 0.35
    axis.barh(positions - bar_height / 2, category["Sales_Amount"], height=bar_height, color=BLUE, label="Sales")
    axis.barh(positions + bar_height / 2, category["Profit"], height=bar_height, color=GREEN, label="Profit")
    axis.set_yticks(positions)
    axis.set_yticklabels(category.index)
    axis.set_title("Sales and Profit by Product_Category", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Amount")
    axis.legend()
    finalize_axis(axis, money_axis="x")
    save_figure(figure, "category_performance.png")


def create_subcategory_performance(dataframe: pd.DataFrame) -> None:
    subcategory = (
        dataframe.groupby("Sub_Category")["Sales_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .sort_values(ascending=True)
    )
    cmap = LinearSegmentedColormap.from_list("sales_gradient", [BLUE, TEAL, GOLD])
    colors = [cmap(i) for i in np.linspace(0.2, 0.95, len(subcategory))]
    figure, axis = plt.subplots(figsize=(12, 7))
    axis.barh(subcategory.index, subcategory.values, color=colors)
    axis.set_title("Top 15 Sub_Category by Sales", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Sales Amount")
    finalize_axis(axis, money_axis="x")
    save_figure(figure, "subcategory_performance.png")


def create_region_sales(dataframe: pd.DataFrame) -> None:
    region = dataframe.groupby("Region")["Sales_Amount"].sum().sort_values(ascending=False)
    figure, axis = plt.subplots(figsize=(8, 8))
    wedges, _texts, _autotexts = axis.pie(
        region.values,
        labels=region.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[PRIMARY, GOLD, GREEN, BLUE, ORANGE, RED],
        wedgeprops={"width": 0.4, "edgecolor": "white"},
        pctdistance=0.8,
    )
    axis.text(0, 0, f"Total\n₹{region.sum():,.0f}", ha="center", va="center", fontsize=14, fontweight="bold", color=PRIMARY)
    axis.set_title("Sales by Region", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.legend(wedges, region.index, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    save_figure(figure, "region_sales.png")


def create_segment_analysis(dataframe: pd.DataFrame) -> None:
    segment = dataframe.groupby("Segment")["Sales_Amount"].sum().sort_values(ascending=False)
    figure, axis = plt.subplots(figsize=(8, 8))
    axis.pie(segment.values, labels=segment.index, autopct="%1.1f%%", startangle=90, colors=[BLUE, GOLD, GREEN, PURPLE])
    axis.set_title("Sales by Segment", fontsize=16, fontweight="bold", color=PRIMARY)
    save_figure(figure, "segment_analysis.png")


def create_top_products(dataframe: pd.DataFrame) -> None:
    top_products = (
        dataframe.groupby("Product Name")["Sales_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )
    figure, axis = plt.subplots(figsize=(12, 7))
    colors = sns.color_palette("Blues_r", n_colors=len(top_products))
    axis.barh(top_products.index, top_products.values, color=colors)
    axis.set_title("Top 10 Product Name by Sales", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Sales Amount")
    finalize_axis(axis, money_axis="x")
    save_figure(figure, "top_products.png")


def create_monthly_heatmap(dataframe: pd.DataFrame) -> None:
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    pivot = (
        dataframe.pivot_table(
            index="Month_Name",
            columns="Year",
            values="Sales_Amount",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(month_order)
        .fillna(0)
    )
    figure, axis = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".0f", linewidths=0.5, ax=axis)
    axis.set_title("Sales by Month vs Year", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Year")
    axis.set_ylabel("Month")
    save_figure(figure, "monthly_heatmap.png")


def create_profit_margin_boxplot(dataframe: pd.DataFrame) -> None:
    figure, axis = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=dataframe, x="Product_Category", y="Profit_Margin", hue="Product_Category", palette=[BLUE, GOLD, GREEN], dodge=False, ax=axis)
    if axis.get_legend() is not None:
        axis.get_legend().remove()
    axis.set_title("Profit_Margin by Product_Category", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Product Category")
    axis.set_ylabel("Profit Margin %")
    finalize_axis(axis)
    save_figure(figure, "profit_margin_boxplot.png")


def create_shipping_analysis(dataframe: pd.DataFrame) -> None:
    shipping = (
        dataframe.groupby("Ship Mode")
        .agg(Avg_Shipping_Days=("Shipping_Days", "mean"), Orders=("Order ID", "nunique"))
        .reset_index()
        .sort_values("Avg_Shipping_Days")
    )
    figure, axis = plt.subplots(figsize=(11, 6))
    bars = axis.bar(shipping["Ship Mode"], shipping["Avg_Shipping_Days"], color=ORANGE, alpha=0.85)
    axis.set_ylabel("Avg Shipping Days")
    axis.set_title("Avg Shipping Days by Ship Mode + Order Count", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.tick_params(axis="x", rotation=20)
    secondary_axis = axis.twinx()
    secondary_axis.plot(shipping["Ship Mode"], shipping["Orders"], color=PRIMARY, marker="o", linewidth=2.2)
    secondary_axis.set_ylabel("Order Count")
    for bar, orders in zip(bars, shipping["Orders"]):
        axis.annotate(f"{orders:,}", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9)
    finalize_axis(axis)
    secondary_axis.spines["top"].set_visible(False)
    save_figure(figure, "shipping_analysis.png")


def create_payment_method(dataframe: pd.DataFrame) -> None:
    payment = dataframe.groupby("Payment_Method")["Sales_Amount"].sum().sort_values(ascending=False)
    figure, axis = plt.subplots(figsize=(8, 8))
    axis.pie(
        payment.values,
        labels=payment.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[TEAL, GOLD, BLUE, ORANGE, PURPLE],
        wedgeprops={"width": 0.42, "edgecolor": "white"},
    )
    axis.text(0, 0, "Payment\nMix", ha="center", va="center", fontsize=14, fontweight="bold", color=PRIMARY)
    axis.set_title("Sales by Payment_Method", fontsize=16, fontweight="bold", color=PRIMARY)
    save_figure(figure, "payment_method.png")


def create_sales_channel(dataframe: pd.DataFrame) -> None:
    channel = dataframe.groupby("Sales_Channel")["Sales_Amount"].sum().sort_values(ascending=False)
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.bar(channel.index, channel.values, color=[BLUE, GOLD, GREEN, ORANGE])
    axis.set_title("Sales by Sales_Channel", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Sales Channel")
    axis.set_ylabel("Sales Amount")
    axis.tick_params(axis="x", rotation=20)
    finalize_axis(axis, money_axis="y")
    save_figure(figure, "sales_channel.png")


def create_state_map(dataframe: pd.DataFrame) -> None:
    states = dataframe.groupby("State")["Sales_Amount"].sum().sort_values(ascending=False).head(10).sort_values()
    figure, axis = plt.subplots(figsize=(12, 7))
    axis.barh(states.index, states.values, color=PURPLE)
    axis.set_title("Top 10 States by Sales", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_xlabel("Sales Amount")
    finalize_axis(axis, money_axis="x")
    save_figure(figure, "state_map.png")


def create_customer_type(dataframe: pd.DataFrame) -> None:
    customer_type = dataframe.groupby("Customer_Type")[["Sales_Amount", "Profit"]].sum().reset_index()
    figure, axis = plt.subplots(figsize=(10, 6))
    positions = np.arange(len(customer_type["Customer_Type"]))
    width = 0.35
    axis.bar(positions - width / 2, customer_type["Sales_Amount"], width=width, label="Sales", color=BLUE)
    axis.bar(positions + width / 2, customer_type["Profit"], width=width, label="Profit", color=GREEN)
    axis.set_xticks(positions)
    axis.set_xticklabels(customer_type["Customer_Type"])
    axis.set_title("Sales & Profit by Customer_Type", fontsize=16, fontweight="bold", color=PRIMARY)
    axis.set_ylabel("Amount")
    axis.legend()
    finalize_axis(axis, money_axis="y")
    save_figure(figure, "customer_type.png")


def create_correlation_heatmap(dataframe: pd.DataFrame) -> None:
    numeric_columns = dataframe.select_dtypes(include=["number"]).copy()
    figure, axis = plt.subplots(figsize=(12, 9))
    sns.heatmap(numeric_columns.corr(), cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, ax=axis)
    axis.set_title("Numeric Column Correlations", fontsize=16, fontweight="bold", color=PRIMARY)
    save_figure(figure, "correlation_heatmap.png")


def create_dashboard_summary(dataframe: pd.DataFrame) -> None:
    monthly = dataframe.groupby("Year_Month")["Sales_Amount"].sum().reset_index().sort_values("Year_Month")
    region = dataframe.groupby("Region")["Sales_Amount"].sum().sort_values(ascending=False)
    category = dataframe.groupby("Product_Category")["Sales_Amount"].sum().sort_values(ascending=False)
    segment = dataframe.groupby("Segment")["Sales_Amount"].sum().sort_values(ascending=False)
    top_products = dataframe.groupby("Product Name")["Sales_Amount"].sum().sort_values(ascending=False).head(8).sort_values()

    positions = np.arange(len(monthly))
    figure, axes = plt.subplots(2, 3, figsize=(18, 10))

    axes[0, 0].plot(positions, monthly["Sales_Amount"], color=BLUE, marker="o")
    axes[0, 0].fill_between(positions, monthly["Sales_Amount"], color=BLUE, alpha=0.15)
    axes[0, 0].set_title("Sales Trend", color=PRIMARY, fontweight="bold")
    tick_step = max(1, len(monthly) // 8)
    axes[0, 0].set_xticks(positions[::tick_step])
    axes[0, 0].set_xticklabels(monthly["Year_Month"].iloc[::tick_step], rotation=45, ha="right")
    finalize_axis(axes[0, 0], money_axis="y")

    axes[0, 1].pie(region.values, labels=region.index, colors=[PRIMARY, GOLD, GREEN, BLUE, ORANGE], wedgeprops={"width": 0.38})
    axes[0, 1].set_title("Region Mix", color=PRIMARY, fontweight="bold")

    axes[0, 2].bar(category.index, category.values, color=[BLUE, GOLD, GREEN])
    axes[0, 2].set_title("Category Sales", color=PRIMARY, fontweight="bold")
    axes[0, 2].tick_params(axis="x", rotation=20)
    finalize_axis(axes[0, 2], money_axis="y")

    axes[1, 0].pie(segment.values, labels=segment.index, colors=[BLUE, GOLD, GREEN, PURPLE], autopct="%1.0f%%")
    axes[1, 0].set_title("Segments", color=PRIMARY, fontweight="bold")

    axes[1, 1].barh(top_products.index, top_products.values, color=sns.color_palette("crest", n_colors=len(top_products)))
    axes[1, 1].set_title("Top Products", color=PRIMARY, fontweight="bold")
    finalize_axis(axes[1, 1], money_axis="x")

    axes[1, 2].hist(dataframe["Profit"], bins=20, color=GREEN, alpha=0.8)
    axes[1, 2].axvline(dataframe["Profit"].mean(), color=RED, linestyle="--", linewidth=2)
    axes[1, 2].set_title("Profit Histogram", color=PRIMARY, fontweight="bold")
    finalize_axis(axes[1, 2], money_axis="x")

    save_figure(figure, "dashboard_summary.png")


def main() -> None:
    """Entry point for chart generation."""
    try:
        configure_console()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        use_style()
        print(f"Reading cleaned dataset: {INPUT_FILE}")
        dataframe = pd.read_csv(INPUT_FILE, parse_dates=["Order Date", "Ship Date"])

        create_sales_trend(dataframe)
        create_profit_distribution(dataframe)
        create_category_performance(dataframe)
        create_subcategory_performance(dataframe)
        create_region_sales(dataframe)
        create_segment_analysis(dataframe)
        create_top_products(dataframe)
        create_monthly_heatmap(dataframe)
        create_profit_margin_boxplot(dataframe)
        create_shipping_analysis(dataframe)
        create_payment_method(dataframe)
        create_sales_channel(dataframe)
        create_state_map(dataframe)
        create_customer_type(dataframe)
        create_correlation_heatmap(dataframe)
        create_dashboard_summary(dataframe)

        print("\nStep 04 completed successfully.")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error in 04_visualizations.py: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
