"""Metrics calculation module for the Superstore dataset."""

import pandas as pd


def calculate_metrics(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate business metrics from the prepared sales DataFrame."""

    required_columns = {
        "Sales",
        "Profit",
        "Quantity",
        "Order ID",
        "Profit Margin Ratio",
        "Is Loss Making",
    }

    missing_columns = required_columns.difference(sales_df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")  # noqa: TRY003

    if sales_df.empty:
        raise ValueError("Empty DataFrame.")  # noqa: TRY003

    # Total metrics
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    total_quantity = sales_df["Quantity"].sum()
    total_order = sales_df["Order ID"].nunique()

    # Row-level averages (each row represents one dataset record)
    average_sales_per_row = sales_df["Sales"].mean()
    average_profit_per_row = sales_df["Profit"].mean()

    # Overall profit margin: total profit divided by total sales
    overall_profit_margin = (
        total_profit / total_sales if total_sales != 0 else float("nan")
    )

    # Profitability metrics
    average_profit_margin_ratio = sales_df["Profit Margin Ratio"].mean()

    loss_making_rows = int(sales_df["Is Loss Making"].eq(True).sum())

    known_profit_rows = sales_df["Profit"].notna().sum()

    loss_making_percentage = (
        loss_making_rows / known_profit_rows * 100
        if known_profit_rows > 0
        else float("nan")
    )

    # Return metrics as a single-row DataFrame
    return pd.DataFrame(
        {
            "Total Sales": [total_sales],
            "Total Profit": [total_profit],
            "Total Quantity Sold": [total_quantity],
            "Average Sales per Row": [average_sales_per_row],
            "Average Profit per Row": [average_profit_per_row],
            "Overall Profit Margin": [overall_profit_margin],
            "Average Profit Margin Ratio": [average_profit_margin_ratio],
            "Loss-Making Rows": [loss_making_rows],
            "Loss-Making Percentage": [loss_making_percentage],
            "Total Orders": [total_order],
        }
    )
