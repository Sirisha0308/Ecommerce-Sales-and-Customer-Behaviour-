import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import os

# ---------------------------
# Load data function
# ---------------------------
@st.cache_data
def load_data():
    zip_path = "cleaned_data_updated.zip"   # Zip file in GitHub
    csv_name = "cleaned_data_updated.csv"   # CSV inside the zip

    if not os.path.exists(csv_name):  # Extract only if not already
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extract(csv_name)

    df = pd.read_csv(csv_name, encoding="latin1")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

# Load dataset
df = load_data()

# ---------------------------
# Sidebar Tabs
# ---------------------------
st.sidebar.title("📂 Dashboard Sections")
tab = st.sidebar.radio(
    "Select Analysis",
    [
        "Dataset Preview",
        "Sales by Country",
        "Top Customers",
        "Sales Over Time",
        "Top Products",
        "Sales by Day of Week",
        "Sales by Month",
        "Yearly Sales Trend",
        "Returns Analysis",
        "Revenue Distribution"
    ]
)

st.title("📊 E-commerce Sales & Customer Behavior Dashboard")

# ---------------------------
# Tab Content
# ---------------------------
if tab == "Dataset Preview":
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

elif tab == "Sales by Country":
    st.subheader("🌍 Sales by Country (Top 10)")
    country_sales = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    country_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Top Customers":
    st.subheader("👥 Top 10 Customers by Sales")
    customer_sales = df.groupby("CustomerID")["TotalPrice"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    customer_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Sales Over Time":
    st.subheader("⏳ Sales Over Time")
    sales_over_time = df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"].sum()
    fig, ax = plt.subplots()
    sales_over_time.plot(ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Top Products":
    st.subheader("📦 Top 10 Products by Sales")
    product_sales = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    product_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Sales by Day of Week":
    st.subheader("📅 Sales by Day of Week")
    day_sales = df.groupby("DayOfWeek")["TotalPrice"].sum()
    fig, ax = plt.subplots()
    day_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Sales by Month":
    st.subheader("🗓️ Sales by Month")
    month_sales = df.groupby("Month")["TotalPrice"].sum()
    fig, ax = plt.subplots()
    month_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Yearly Sales Trend":
    st.subheader("📊 Yearly Sales Trend")
    year_sales = df.groupby("Year")["TotalPrice"].sum()
    fig, ax = plt.subplots()
    year_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Returns Analysis":
    st.subheader("🔄 Returns Analysis")
    return_sales = df.groupby("is_return")["TotalPrice"].sum()
    fig, ax = plt.subplots()
    return_sales.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total Sales")
    st.pyplot(fig)

elif tab == "Revenue Distribution":
    st.subheader("💰 Revenue Distribution")
    fig, ax = plt.subplots()
    df["TotalPrice"].plot(kind="hist", bins=50, ax=ax)
    ax.set_xlabel("TotalPrice")
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Developed by Sirisha")