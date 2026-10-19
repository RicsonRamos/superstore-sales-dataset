"""Streamlit application for the Superstore Sales Dashboard."""

import pandas as pd
import streamlit as st

from superstore_sales_dataset.data_clean import data_prepare
from superstore_sales_dataset.data_loader import load_data
from superstore_sales_dataset.metrics import calculate_metrics

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def get_prepared_data() -> pd.DataFrame:
    """Load and prepare the original dataset in memory."""

    raw_data_path = load_data()

    sales_df = pd.read_csv(
        raw_data_path,
        encoding="ISO-8859-1",
        dtype={"Postal Code": "string"},
    )

    return data_prepare(sales_df)


def main() -> None:
    """Render the Superstore Sales Dashboard."""

    st.title("Superstore Sales Dashboard")
    st.caption("Sales performance, profitability, and loss analysis")

    # Load and prepare data
    try:
        sales_df = get_prepared_data()
    except Exception as exc:
        st.error(f"Unable to load or prepare the dataset: {exc}")
        st.exception(exc)
        st.stop()

    if sales_df.empty:
        st.warning("The dataset contains no records after preparation.")
        st.stop()

    # Calculate metrics using the dedicated metrics module
    try:
        metrics_df = calculate_metrics(sales_df)
        metrics = metrics_df.iloc[0]
    except Exception as exc:
        st.error(f"Unable to calculate metrics: {exc}")
        st.exception(exc)
        st.stop()

    # Main KPIs
    st.subheader("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sales",
        f"${metrics['Total Sales']:,.2f}",
    )

    col2.metric(
        "Total Profit",
        f"${metrics['Total Profit']:,.2f}",
    )

    col3.metric(
        "Overall Profit Margin",
        (
            f"{metrics['Overall Profit Margin']:.2%}"
            if pd.notna(metrics["Overall Profit Margin"])
            else "N/A"
        ),
    )

    col4.metric(
        "Total Orders",
        f"{metrics['Total Orders']}",
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Quantity Sold",
        f"{metrics['Total Quantity Sold']:,.0f}",
    )

    col6.metric(
        "Average Sales per Row",
        (
            f"${metrics['Average Sales per Row']:,.2f}"
            if pd.notna(metrics["Average Sales per Row"])
            else "N/A"
        ),
    )

    col7.metric(
        "Average Profit per Row",
        (
            f"${metrics['Average Profit per Row']:,.2f}"
            if pd.notna(metrics["Average Profit per Row"])
            else "N/A"
        ),
    )

    col8.metric(
        "Loss-Making Rows",
        f"{metrics['Loss-Making Rows']:,.0f}",
    )

    st.divider()

    # Sidebar filters
    st.sidebar.header("Dashboard Filters")

    filtered_df = sales_df.copy()

    if "Order Date" in filtered_df.columns:
        valid_dates = filtered_df["Order Date"].dropna()

        if not valid_dates.empty:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            selected_dates = st.sidebar.date_input(
                "Order Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

            if isinstance(selected_dates, tuple | list) and len(selected_dates) == 2:
                start_date, end_date = selected_dates

                filtered_df = filtered_df[
                    filtered_df["Order Date"].isna()
                    | (
                        filtered_df["Order Date"].dt.date.between(
                            start_date,
                            end_date,
                        )
                    )
                ]

    if "Region" in filtered_df.columns:
        regions = sorted(filtered_df["Region"].dropna().unique().tolist())

        selected_regions = st.sidebar.multiselect(
            "Region",
            options=regions,
            default=regions,
        )

        filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]

    if "Category" in filtered_df.columns:
        categories = sorted(filtered_df["Category"].dropna().unique().tolist())

        selected_categories = st.sidebar.multiselect(
            "Category",
            options=categories,
            default=categories,
        )

        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]

    st.caption(f"Records matching filters: {len(filtered_df):,}")

    # Recalculate metrics for the filtered dataset
    if filtered_df.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    filtered_metrics_df = calculate_metrics(filtered_df)
    filtered_metrics = filtered_metrics_df.iloc[0]

    st.subheader("Filtered Performance")

    filtered_col1, filtered_col2, filtered_col3 = st.columns(3)

    filtered_col1.metric(
        "Filtered Sales",
        f"${filtered_metrics['Total Sales']:,.2f}",
    )

    filtered_col2.metric(
        "Filtered Profit",
        f"${filtered_metrics['Total Profit']:,.2f}",
    )

    filtered_col3.metric(
        "Filtered Profit Margin",
        (
            f"{filtered_metrics['Overall Profit Margin']:.2%}"
            if pd.notna(filtered_metrics["Overall Profit Margin"])
            else "N/A"
        ),
    )

    st.divider()

    # Sales over time
    st.subheader("Sales Over Time")

    sales_by_date = (
        filtered_df.dropna(subset=["Order Date", "Sales"])
        .assign(
            Month=lambda data: data["Order Date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    if not sales_by_date.empty:
        st.line_chart(sales_by_date)
    else:
        st.info("No valid dates or sales values are available for this chart.")

    # Profit by category
    if "Category" in filtered_df.columns:
        st.subheader("Profit by Category")

        profit_by_category = (
            filtered_df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
        )

        st.bar_chart(profit_by_category)

    # Profit by region
    if "Region" in filtered_df.columns:
        st.subheader("Profit by Region")

        profit_by_region = (
            filtered_df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
        )

        st.bar_chart(profit_by_region)

    # Loss-making records
    st.subheader("Loss-Making Records")

    loss_df = filtered_df.loc[filtered_df["Is Loss Making"].eq(True)]

    st.caption(f"Records with negative profit: {len(loss_df):,}")

    st.dataframe(
        loss_df,
        width="stretch",
        hide_index=True,
    )

    # Prepared data and metrics
    with st.expander("View calculated metrics"):
        st.dataframe(
            filtered_metrics_df,
            width="stretch",
            hide_index=True,
        )

    with st.expander("View prepared dataset"):
        st.dataframe(
            filtered_df,
            width="stretch",
            hide_index=True,
        )


if __name__ == "__main__":
    main()
