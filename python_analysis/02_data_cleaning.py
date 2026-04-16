"""Clean the sales dataset and derive analysis-ready columns."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(r"C:\anil")
INPUT_FILE = BASE_DIR / "generated_sales_data.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"
EXPECTED_COLUMNS = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Ship Date",
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country",
    "City",
    "State",
    "Postal Code",
    "Region",
    "Product ID",
    "Product_Category",
    "Sub_Category",
    "Product Name",
    "Sales_Amount",
    "Unit_Price",
    "Unit_Cost",
    "Sales_Channel",
    "Payment_Method",
    "Customer_Type",
    "Quantity",
    "Profit",
]
NUMERIC_COLUMNS = ["Sales_Amount", "Unit_Price", "Unit_Cost", "Quantity", "Profit", "Postal Code"]


def configure_console() -> None:
    """Enable UTF-8 console output where supported."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def fill_missing_values(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values with median and categorical values with mode."""
    print("\nMissing Values Per Column:")
    print(dataframe.isna().sum().to_string())

    for column in NUMERIC_COLUMNS:
        if column in dataframe.columns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")
            median_value = dataframe[column].median()
            dataframe[column] = dataframe[column].fillna(median_value)

    categorical_columns = [
        column
        for column in dataframe.columns
        if column not in NUMERIC_COLUMNS and column not in {"Order Date", "Ship Date"}
    ]
    for column in categorical_columns:
        mode_series = dataframe[column].mode(dropna=True)
        fill_value = mode_series.iloc[0] if not mode_series.empty else "Unknown"
        dataframe[column] = dataframe[column].fillna(fill_value)

    return dataframe


def add_derived_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Add calculated columns required for analysis."""
    sales_amount = dataframe["Sales_Amount"].replace(0, np.nan)
    dataframe["Profit_Margin"] = np.where(
        sales_amount.notna(),
        (dataframe["Profit"] / sales_amount) * 100,
        0.0,
    )
    dataframe["Profit_Margin"] = dataframe["Profit_Margin"].replace([np.inf, -np.inf], 0).fillna(0)

    dataframe["Month"] = dataframe["Order Date"].dt.month
    dataframe["Month_Name"] = dataframe["Order Date"].dt.month_name()
    dataframe["Year"] = dataframe["Order Date"].dt.year
    dataframe["Quarter"] = "Q" + dataframe["Order Date"].dt.quarter.fillna(0).astype(int).astype(str)
    dataframe["Quarter"] = dataframe["Quarter"].replace({"Q0": np.nan})
    dataframe["Day_of_Week"] = dataframe["Order Date"].dt.day_name()
    dataframe["Year_Month"] = dataframe["Order Date"].dt.strftime("%Y-%m")
    dataframe["Shipping_Days"] = (dataframe["Ship Date"] - dataframe["Order Date"]).dt.days

    margin_conditions = [
        dataframe["Profit_Margin"] > 30,
        dataframe["Profit_Margin"].between(10, 30, inclusive="both"),
        dataframe["Profit_Margin"].between(0, 10, inclusive="left"),
        dataframe["Profit_Margin"] < 0,
    ]
    margin_labels = ["High (>30%)", "Medium (10-30%)", "Low (0-10%)", "Loss (<0%)"]
    dataframe["Margin_Category"] = np.select(margin_conditions, margin_labels, default="Low (0-10%)")

    return dataframe


def main() -> None:
    """Entry point for dataset cleaning."""
    try:
        configure_console()
        print(f"Reading input file: {INPUT_FILE}")
        dataframe = pd.read_csv(INPUT_FILE)

        extra_columns = [column for column in dataframe.columns if column not in EXPECTED_COLUMNS]
        if extra_columns:
            print(f"\nDropping unexpected columns: {extra_columns}")
            dataframe = dataframe.drop(columns=extra_columns)

        dataframe = fill_missing_values(dataframe)

        before_dedup = len(dataframe)
        dataframe = dataframe.drop_duplicates(subset=["Order ID"], keep="first").copy()
        after_dedup = len(dataframe)
        print(f"\nRemoved duplicate Order IDs: {before_dedup - after_dedup:,}")

        dataframe["Order Date"] = pd.to_datetime(dataframe["Order Date"], dayfirst=True, errors="coerce")
        dataframe["Ship Date"] = pd.to_datetime(dataframe["Ship Date"], dayfirst=True, errors="coerce")

        for column in ["Sales_Amount", "Unit_Price", "Unit_Cost", "Quantity", "Profit"]:
            dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")
            dataframe[column] = dataframe[column].fillna(dataframe[column].median())

        dataframe = add_derived_columns(dataframe)

        dataframe.to_csv(OUTPUT_FILE, index=False)
        print(f"\nCleaned file saved to: {OUTPUT_FILE}")
        print(f"Final Shape: {dataframe.shape}")
        print("\nFinal Columns and Data Types:")
        for column_name, dtype in dataframe.dtypes.items():
            print(f" - {column_name}: {dtype}")

        print("\nStep 02 completed successfully.")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error in 02_data_cleaning.py: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
