"""Load the source dataset, validate schema, and create a backup copy."""

from __future__ import annotations

import shutil
import sys
from io import StringIO
from pathlib import Path

import pandas as pd


BASE_DIR = Path(r"C:\anil")
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


def configure_console() -> None:
    """Enable UTF-8 console output where supported."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def resolve_source_file() -> Path:
    """Prefer sales.csv, but fall back to dataset.csv if needed."""
    sales_path = BASE_DIR / "sales.csv"
    dataset_path = BASE_DIR / "dataset.csv"

    if sales_path.exists():
        return sales_path
    if dataset_path.exists():
        print("Warning: C:\\anil\\sales.csv not found. Using C:\\anil\\dataset.csv instead.")
        return dataset_path

    raise FileNotFoundError("Neither sales.csv nor dataset.csv was found in C:\\anil")


def print_basic_info(dataframe: pd.DataFrame) -> None:
    """Print overview details for the loaded dataframe."""
    print(f"\nDataset Shape: {dataframe.shape}")
    print("\nColumns:")
    for column in dataframe.columns:
        print(f" - {column}")

    print("\nData Types:")
    print(dataframe.dtypes.to_string())

    print("\nFirst 5 Rows:")
    print(dataframe.head().to_string())

    buffer = StringIO()
    dataframe.info(buf=buffer)
    print("\nBasic Info:")
    print(buffer.getvalue())


def print_summary_stats(dataframe: pd.DataFrame) -> None:
    """Print the requested summary statistics."""
    order_dates = pd.to_datetime(dataframe["Order Date"], dayfirst=True, errors="coerce")
    date_min = order_dates.min()
    date_max = order_dates.max()

    print("\nSummary Statistics")
    print("-" * 60)
    print(f"Total Records     : {len(dataframe):,}")
    print(f"Date Range        : {date_min.date() if pd.notna(date_min) else 'N/A'} to {date_max.date() if pd.notna(date_max) else 'N/A'}")
    print(f"Unique Customers  : {dataframe['Customer ID'].nunique(dropna=True):,}")
    print(f"Unique Products   : {dataframe['Product ID'].nunique(dropna=True):,}")
    print(f"Regions           : {', '.join(sorted(map(str, dataframe['Region'].dropna().unique())))}")
    print(f"Segments          : {', '.join(sorted(map(str, dataframe['Segment'].dropna().unique())))}")


def main() -> None:
    """Entry point for dataset loading."""
    try:
        configure_console()
        source_file = resolve_source_file()
        backup_file = BASE_DIR / "generated_sales_data.csv"

        print(f"Reading source file: {source_file}")
        dataframe = pd.read_csv(source_file)

        print_basic_info(dataframe)

        missing_columns = [column for column in EXPECTED_COLUMNS if column not in dataframe.columns]
        if missing_columns:
            print("\nWarning: Missing expected columns:")
            for column in missing_columns:
                print(f" - {column}")
        else:
            print("\nAll expected columns are present.")

        shutil.copy2(source_file, backup_file)
        print(f"\nBackup copy created at: {backup_file}")

        print_summary_stats(dataframe)
        print("\nStep 01 completed successfully.")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error in 01_generate_or_load_dataset.py: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
