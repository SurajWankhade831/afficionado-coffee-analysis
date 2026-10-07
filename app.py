import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Afficionado Coffee Roasters Sales Dashboard",
    page_icon="☕",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

file_path = "data/Afficionado Coffee Roasters.xlsx"

# Explicitly use openpyxl for Excel files
df = pd.read_excel(
    file_path,
    engine="openpyxl"
)


# ============================================================
# DATA PREPARATION
# ============================================================

# Convert transaction time
df["transaction_time"] = pd.to_datetime(
    df["transaction_time"],
    format="%H:%M:%S",
    errors="coerce"
)

# Extract hour
df["hour"] = df["transaction_time"].dt.hour

# Calculate revenue
df["revenue"] = (
    df["transaction_qty"] *
    df["unit_price"]
)


# ============================================================
# TITLE
# ============================================================

st.title("☕ Afficionado Coffee Roasters")
st.subheader("Sales Trend and Time-Based Performance Analysis")

st.markdown(
    """
    This interactive dashboard analyzes transaction-level sales data
    to identify hourly demand patterns, store performance, product
    performance, and business opportunities.
    """
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

# Store filter
store_options = sorted(
    df["store_location"].dropna().unique()
)

selected_stores = st.sidebar.multiselect(
    "Select Store Location",
    options=store_options,
    default=store_options
)

# Product category filter
category_options = sorted(
    df["product_category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=category_options,
    default=category_options
)

# Hour filter
min_hour = int(df["hour"].min())
max_hour = int(df["hour"].max())

selected_hours = st.sidebar.slider(
    "Select Hour Range",
    min_value=min_hour,
    max_value=max_hour,
    value=(min_hour, max_hour)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["store_location"].isin(selected_stores)) &
    (df["product_category"].isin(selected_categories)) &
    (df["hour"].between(selected_hours[0], selected_hours[1]))
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["revenue"].sum()

total_quantity = filtered_df["transaction_qty"].sum()

total_transactions = filtered_df["transaction_id"].nunique()

average_transaction_value = (
    total_revenue / total_transactions
    if total_transactions > 0
    else 0
)


# ============================================================
# KPI DISPLAY
# ============================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "📦 Quantity Sold",
        f"{total_quantity:,.0f}"
    )

with col3:
    st.metric(
        "🧾 Transactions",
        f"{total_transactions:,.0f}"
    )

with col4:
    st.metric(
        "🛒 Avg. Transaction Value",
        f"${average_transaction_value:,.2f}"
    )


# ============================================================
# SECTION 1 — HOURLY PERFORMANCE
# ============================================================

st.markdown("---")

st.header("⏰ Hourly Sales Performance")

hourly_revenue = (
    filtered_df
    .groupby("hour")["revenue"]
    .sum()
    .sort_index()
)

hourly_quantity = (
    filtered_df
    .groupby("hour")["transaction_qty"]
    .sum()
    .sort_index()
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Revenue by Hour
# ------------------------------------------------------------

with col1:

    st.subheader("Revenue by Hour")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        hourly_revenue.index,
        hourly_revenue.values,
        marker="o"
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Revenue by Hour")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# Quantity by Hour
# ------------------------------------------------------------

with col2:

    st.subheader("Quantity Sold by Hour")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        hourly_quantity.index,
        hourly_quantity.values
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Quantity Sold")
    ax.set_title("Quantity Sold by Hour")

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# PEAK HOUR
# ============================================================

if not hourly_revenue.empty:

    peak_hour = hourly_revenue.idxmax()
    peak_revenue = hourly_revenue.max()

    lowest_hour = hourly_revenue.idxmin()
    lowest_revenue = hourly_revenue.min()

    st.info(
        f"📈 **Peak Revenue Hour:** {peak_hour}:00 "
        f"with ${peak_revenue:,.2f} revenue."
    )

    st.warning(
        f"📉 **Lowest Revenue Hour:** {lowest_hour}:00 "
        f"with ${lowest_revenue:,.2f} revenue."
    )


# ============================================================
# SECTION 2 — STORE PERFORMANCE
# ============================================================

st.markdown("---")

st.header("🏪 Store Performance")


store_revenue = (
    filtered_df
    .groupby("store_location")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

store_quantity = (
    filtered_df
    .groupby("store_location")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Store Revenue
# ------------------------------------------------------------

with col1:

    st.subheader("Revenue by Store")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        store_revenue.index,
        store_revenue.values
    )

    ax.set_xlabel("Store Location")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Revenue by Store")

    plt.xticks(rotation=20)

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# Store Quantity
# ------------------------------------------------------------

with col2:

    st.subheader("Quantity Sold by Store")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        store_quantity.index,
        store_quantity.values
    )

    ax.set_xlabel("Store Location")
    ax.set_ylabel("Quantity Sold")
    ax.set_title("Quantity Sold by Store")

    plt.xticks(rotation=20)

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# STORE PERFORMANCE TABLE
# ============================================================

store_summary = (
    filtered_df
    .groupby("store_location")
    .agg(
        Revenue=("revenue", "sum"),
        Quantity=("transaction_qty", "sum"),
        Transactions=("transaction_id", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

st.subheader("Store Performance Summary")

st.dataframe(
    store_summary.style.format(
        {
            "Revenue": "${:,.2f}",
            "Quantity": "{:,.0f}",
            "Transactions": "{:,.0f}"
        }
    ),
    use_container_width=True
)


# ============================================================
# SECTION 3 — PRODUCT CATEGORY PERFORMANCE
# ============================================================

st.markdown("---")

st.header("📦 Product Category Performance")


category_revenue = (
    filtered_df
    .groupby("product_category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

category_quantity = (
    filtered_df
    .groupby("product_category")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Category Revenue
# ------------------------------------------------------------

with col1:

    st.subheader("Revenue by Product Category")

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        category_revenue.index[::-1],
        category_revenue.values[::-1]
    )

    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Product Category")
    ax.set_title("Revenue by Product Category")

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# Category Quantity
# ------------------------------------------------------------

with col2:

    st.subheader("Quantity by Product Category")

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        category_quantity.index[::-1],
        category_quantity.values[::-1]
    )

    ax.set_xlabel("Quantity Sold")
    ax.set_ylabel("Product Category")
    ax.set_title("Quantity by Product Category")

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# SECTION 4 — PRODUCT TYPE PERFORMANCE
# ============================================================

st.markdown("---")

st.header("☕ Product Type Performance")


product_type_revenue = (
    filtered_df
    .groupby("product_type")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

product_type_quantity = (
    filtered_df
    .groupby("product_type")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Top Product Types by Revenue
# ------------------------------------------------------------

with col1:

    st.subheader("Top 10 Product Types by Revenue")

    top_revenue_types = (
        product_type_revenue
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        top_revenue_types.index,
        top_revenue_types.values
    )

    ax.set_xlabel("Revenue ($)")
    ax.set_title("Top 10 Product Types by Revenue")

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# Top Product Types by Quantity
# ------------------------------------------------------------

with col2:

    st.subheader("Top 10 Product Types by Quantity")

    top_quantity_types = (
        product_type_quantity
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        top_quantity_types.index,
        top_quantity_types.values
    )

    ax.set_xlabel("Quantity Sold")
    ax.set_title("Top 10 Product Types by Quantity")

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# SECTION 5 — TOP PRODUCTS
# ============================================================

st.markdown("---")

st.header("🏆 Top Products")


product_quantity = (
    filtered_df
    .groupby("product_detail")["transaction_qty"]
    .sum()
    .sort_values(ascending=False)
)

product_revenue = (
    filtered_df
    .groupby("product_detail")["revenue"]
    .sum()
    .sort_values(ascending=False)
)


col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Top Products by Quantity
# ------------------------------------------------------------

with col1:

    st.subheader("Top 10 Products by Quantity")

    top_products_quantity = (
        product_quantity
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        top_products_quantity.index,
        top_products_quantity.values
    )

    ax.set_xlabel("Quantity Sold")
    ax.set_title("Top 10 Products by Quantity")

    st.pyplot(fig)

    plt.close(fig)


# ------------------------------------------------------------
# Top Products by Revenue
# ------------------------------------------------------------

with col2:

    st.subheader("Top 10 Products by Revenue")

    top_products_revenue = (
        product_revenue
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        top_products_revenue.index,
        top_products_revenue.values
    )

    ax.set_xlabel("Revenue ($)")
    ax.set_title("Top 10 Products by Revenue")

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# SECTION 6 — STORE × HOUR ANALYSIS
# ============================================================

st.markdown("---")

st.header("🔥 Store and Hour Analysis")

store_hour_revenue = (
    filtered_df
    .groupby(
        ["store_location", "hour"]
    )["revenue"]
    .sum()
    .unstack(fill_value=0)
)


if not store_hour_revenue.empty:

    fig, ax = plt.subplots(figsize=(12, 6))

    image = ax.imshow(
        store_hour_revenue,
        aspect="auto",
        cmap="viridis"
    )

    fig.colorbar(
        image,
        ax=ax,
        label="Revenue ($)"
    )

    ax.set_xticks(
        range(len(store_hour_revenue.columns))
    )

    ax.set_xticklabels(
        store_hour_revenue.columns
    )

    ax.set_yticks(
        range(len(store_hour_revenue.index))
    )

    ax.set_yticklabels(
        store_hour_revenue.index
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Store Location")

    ax.set_title(
        "Revenue by Store and Hour"
    )

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# SECTION 7 — KEY BUSINESS INSIGHTS
# ============================================================

st.markdown("---")

st.header("💡 Key Business Insights")


# Overall peak
if not hourly_revenue.empty:

    overall_peak_hour = hourly_revenue.idxmax()
    overall_peak_value = hourly_revenue.max()

else:

    overall_peak_hour = None
    overall_peak_value = 0


# Top store
if not store_revenue.empty:

    top_store = store_revenue.idxmax()
    top_store_value = store_revenue.max()

else:

    top_store = "N/A"
    top_store_value = 0


# Top category
if not category_revenue.empty:

    top_category = category_revenue.idxmax()
    top_category_value = category_revenue.max()

else:

    top_category = "N/A"
    top_category_value = 0


col1, col2, col3 = st.columns(3)


with col1:

    st.success(
        f"""
        **Peak Sales Hour**

        {overall_peak_hour}:00

        Revenue: ${overall_peak_value:,.2f}
        """
    )


with col2:

    st.success(
        f"""
        **Top Store**

        {top_store}

        Revenue: ${top_store_value:,.2f}
        """
    )


with col3:

    st.success(
        f"""
        **Top Category**

        {top_category}

        Revenue: ${top_category_value:,.2f}
        """
    )


# ============================================================
# BUSINESS RECOMMENDATIONS
# ============================================================

st.markdown("---")

st.header("📌 Business Recommendations")

st.markdown(
    """
    **1. Optimize staffing during peak morning hours**

    Sales are strongest during the morning period, particularly
    around 8:00 AM–10:00 AM. Staffing levels should be aligned
    with this demand pattern.

    **2. Focus operational attention on high-performing stores**

    Store-level revenue differences can be used to improve staffing,
    inventory planning, and store-specific operational decisions.

    **3. Prioritize high-performing product categories**

    Coffee and Tea generate substantial revenue and should receive
    appropriate inventory and promotional attention.

    **4. Review late-evening operating efficiency**

    Revenue decreases considerably during the late evening.
    Management can evaluate staffing and operating costs during
    low-demand hours.

    **5. Use product-level sales data for inventory planning**

    High-volume products should receive priority in inventory
    replenishment to reduce the risk of stockouts.
    """
)


# ============================================================
# DATA LIMITATION
# ============================================================

st.markdown("---")

st.header("⚠️ Dataset Limitation")

st.info(
    """
    The dataset contains transaction time but does not contain an
    actual transaction date. Therefore, genuine day-of-week,
    monthly, or date-based sales trends cannot be calculated from
    the available data.

    This dashboard therefore focuses on hourly, store-level,
    category-level, product-level, and store-hour performance.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Afficionado Coffee Roasters – Sales Trend and "
    "Time-Based Performance Analysis"
)