import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales KPI Dashboard")

# Upload File
uploaded_file = st.file_uploader("Upload Sales Dataset", type=["csv"])

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)

    # Date Conversion
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    category = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    # Filter Data
    filtered_df = df[
        (df["Region"].isin(region)) &
        (df["Category"].isin(category))
    ]

    # KPI Calculations
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df.shape[0]
    avg_order_value = total_sales / total_orders

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
    col3.metric("🛒 Total Orders", f"{total_orders:,}")
    col4.metric("📦 Avg Order Value", f"${avg_order_value:,.2f}")

    st.markdown("---")

    # Sales Trend
    sales_trend = (
        filtered_df.groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        sales_trend,
        x="Order Date",
        y="Sales",
        title="Sales Trend"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # Charts Row
    col5, col6 = st.columns(2)

    with col5:
        region_sales = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            title="Sales by Region",
            text_auto=True
        )

        st.plotly_chart(fig_region, use_container_width=True)

    with col6:
        category_sales = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig_category = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            title="Category Contribution"
        )

        st.plotly_chart(fig_category, use_container_width=True)

    # Top Products
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top Products by Sales"
    )

    st.plotly_chart(fig_products, use_container_width=True)

    # Detailed Data
    st.subheader("📋 Sales Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Please upload a sales CSV file.")