"""Data cleaning and preparation module."""

import pandas as pd


class MissingRequiredColumnsError(ValueError):
    """Raised when required dataset columns are missing."""

    def __init__(self, columns: list[str]) -> None:
        self.columns = columns
        super().__init__(f"Missing required dataset columns: {columns}")


def data_prepare(sales_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare Superstore sales data in memory."""

    sales_df = sales_df.copy()

    # Validate required columns.
    required_columns = {
        "Order Date",
        "Ship Date",
        "Postal Code",
        "Row ID",
        "Sales",
        "Profit",
    }

    missing_columns = required_columns.difference(sales_df.columns)

    if missing_columns:
        raise MissingRequiredColumnsError(sorted(missing_columns))
    # Convert dates to datetime.
    for column in ["Order Date", "Ship Date"]:
        sales_df[column] = pd.to_datetime(
            sales_df[column],
            errors="coerce",
        )

    # Preserve postal codes as text, including leading zeros
    # that are present in the original CSV.
    postal_code = sales_df["Postal Code"].astype("string")
    sales_df["Postal Code"] = postal_code.str.replace(
        r"\.0$",
        "",
        regex=True,
    )

    # Convert financial columns to numeric values.
    for column in ["Sales", "Profit"]:
        sales_df[column] = pd.to_numeric(
            sales_df[column],
            errors="coerce",
        )

    # Warn about invalid shipping dates.
    invalid_shipping_dates = (
        sales_df["Ship Date"].notna()
        & sales_df["Order Date"].notna()
        & sales_df["Ship Date"].lt(sales_df["Order Date"])
    )

    if invalid_shipping_dates.any():
        print("Warning: Some rows have Ship Date earlier than Order Date.")

    # Remove duplicate row identifiers.
    sales_df = sales_df.drop_duplicates(
        subset=["Row ID"],
        keep="first",
    )

    # Required feature: profit margin ratio.
    # A zero or missing Sales value results in a missing ratio.
    sales_df["Profit Margin Ratio"] = sales_df["Profit"].div(
        sales_df["Sales"].where(sales_df["Sales"].ne(0))
    )

    # Required feature: whether the row represents a loss.
    # Missing Profit values remain unknown rather than being classified
    # as profitable.
    sales_df["Is Loss Making"] = pd.Series(
        pd.NA,
        index=sales_df.index,
        dtype="boolean",
    )

    known_profit = sales_df["Profit"].notna()

    sales_df.loc[known_profit, "Is Loss Making"] = (
        sales_df.loc[known_profit, "Profit"] < 0
    )

    # Sort by order date.
    return sales_df.sort_values(
        by="Order Date",
        na_position="last",
    ).reset_index(drop=True)
