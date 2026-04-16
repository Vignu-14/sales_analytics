"""Forecast future monthly sales using linear regression."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
except ImportError:  # pragma: no cover - lightweight fallback
    class LinearRegression:  # type: ignore[override]
        """Fallback linear regression using NumPy polyfit."""

        def fit(self, x_values, y_values):
            x_array = np.asarray(x_values).reshape(-1)
            y_array = np.asarray(y_values)
            slope, intercept = np.polyfit(x_array, y_array, 1)
            self.coef_ = np.array([slope])
            self.intercept_ = intercept
            return self

        def predict(self, x_values):
            x_array = np.asarray(x_values).reshape(-1)
            return (self.coef_[0] * x_array) + self.intercept_

    def mean_squared_error(y_true, y_pred, squared=True):
        error = np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)
        return error if squared else np.sqrt(error)

    def r2_score(y_true, y_pred):
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot if ss_tot else 0)


BASE_DIR = Path(r"C:\anil")
INPUT_FILE = BASE_DIR / "cleaned_sales_data.csv"
OUTPUT_FILE = BASE_DIR / "python_analysis" / "output_charts" / "forecast.png"


def configure_console() -> None:
    """Enable UTF-8 console output where supported."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def money_formatter(value: float, _position: float) -> str:
    return f"₹{value:,.0f}"


def build_monthly_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        dataframe.groupby("Year_Month")["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Year_Month")
        .rename(columns={"Sales_Amount": "Actual_Sales"})
    )
    monthly["Month_Date"] = pd.to_datetime(monthly["Year_Month"] + "-01")
    monthly["Time_Index"] = np.arange(1, len(monthly) + 1)
    monthly["MA_3"] = monthly["Actual_Sales"].rolling(window=3).mean()
    monthly["MA_6"] = monthly["Actual_Sales"].rolling(window=6).mean()
    return monthly


def main() -> None:
    """Entry point for forecasting."""
    try:
        configure_console()
        print(f"Reading cleaned dataset: {INPUT_FILE}")
        dataframe = pd.read_csv(INPUT_FILE, parse_dates=["Order Date", "Ship Date"])
        monthly = build_monthly_frame(dataframe)

        model = LinearRegression()
        x_values = monthly[["Time_Index"]]
        y_values = monthly["Actual_Sales"]
        model.fit(x_values, y_values)

        monthly["Trend_Line"] = model.predict(x_values)

        future_index = np.arange(len(monthly) + 1, len(monthly) + 7)
        future_months = pd.date_range(monthly["Month_Date"].max() + pd.offsets.MonthBegin(1), periods=6, freq="MS")
        future_predictions = model.predict(future_index.reshape(-1, 1))
        lower_band = future_predictions * 0.85
        upper_band = future_predictions * 1.15

        r_squared = r2_score(y_values, monthly["Trend_Line"])
        rmse = mean_squared_error(y_values, monthly["Trend_Line"], squared=False)
        slope = float(model.coef_[0])
        intercept = float(model.intercept_)

        forecast_table = pd.DataFrame(
            {
                "Month": future_months.strftime("%Y-%m"),
                "Predicted_Sales": future_predictions,
                "Lower_Bound": lower_band,
                "Upper_Bound": upper_band,
            }
        )

        figure, axis = plt.subplots(figsize=(13, 7))
        axis.plot(monthly["Month_Date"], monthly["Actual_Sales"], color="#3498DB", marker="o", linewidth=2.5, label="Actual Sales")
        axis.plot(monthly["Month_Date"], monthly["Trend_Line"], color="#1B2A4A", linestyle="--", linewidth=2.2, label="Trend Line")
        axis.plot(monthly["Month_Date"], monthly["MA_3"], color="#F4B942", linewidth=2, label="3-Month MA")
        axis.plot(monthly["Month_Date"], monthly["MA_6"], color="#2ECC71", linewidth=2, label="6-Month MA")
        axis.plot(future_months, future_predictions, color="#E67E22", marker="D", linewidth=2.2, label="6-Month Forecast")
        axis.fill_between(future_months, lower_band, upper_band, color="#E67E22", alpha=0.18, label="Confidence Band (±15%)")
        axis.set_title("Sales Forecast with Trend and Moving Averages", fontsize=16, fontweight="bold", color="#1B2A4A")
        axis.set_xlabel("Month")
        axis.set_ylabel("Sales Amount")
        axis.yaxis.set_major_formatter(FuncFormatter(money_formatter))
        axis.grid(alpha=0.25)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.legend()
        figure.tight_layout()
        figure.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")
        plt.close(figure)

        print("\nForecast Table")
        print("-" * 70)
        print(
            forecast_table.to_string(
                index=False,
                formatters={
                    "Predicted_Sales": "₹{:,.2f}".format,
                    "Lower_Bound": "₹{:,.2f}".format,
                    "Upper_Bound": "₹{:,.2f}".format,
                },
            )
        )

        print("\nModel Metrics")
        print("-" * 70)
        print(f"R²        : {r_squared:.4f}")
        print(f"RMSE      : ₹{rmse:,.2f}")
        print(f"Slope     : {slope:,.2f}")
        print(f"Intercept : {intercept:,.2f}")
        print(f"\nForecast chart saved to: {OUTPUT_FILE}")
        print("\nStep 05 completed successfully.")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error in 05_forecasting.py: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
