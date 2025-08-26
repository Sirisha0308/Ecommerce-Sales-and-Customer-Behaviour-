import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="E-commerce Sales & Customer Behaviour Analysis",
    layout="wide"
)

st.title("📊 E-commerce Sales & Customer Behaviour Analysis")

# -------------------------------
# Load dataset
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "cleaned_dataset_updated.zip",
        compression="zip",
        encoding="ISO-8859-1",
        low_memory=False
    )
    return df

df = load_data()

# -------------------------------
# Data Cleaning
# -------------------------------
df["is_return"] = df["Quantity"] < 0
df = df[df["UnitPrice"] > 0]
df = df.dropna(subset=["Description", "CustomerID"])
df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Add Total Sales column
df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

st.success("✅ Data successfully loaded and cleaned!")

# -------------------------------
# Tabs for navigation
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Sales Overview", "🛍 Customer Behaviour", "🔄 Returns Analysis", "📦 Top Products"]
)

# -------------------------------
# Tab 1: Sales Overview
# -------------------------------
with tab1:
    st.header("Sales Overview")

    # Sales over time
    sales_time = df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalSales"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    sales_time.plot(kind="line", marker="o", ax=ax)
    ax.set_title("Monthly Sales Over Time")
    ax.set_ylabel("Total Sales")
    ax.set_xlabel("Month")
    st.pyplot(fig)

    # Country-wise sales
    country_sales = df.groupby("Country")["TotalSales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=country_sales.values, y=country_sales.index, ax=ax)
    ax.set_title("Top 10 Countries by Sales")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# -------------------------------
# Tab 2: Customer Behaviour
# -------------------------------
with tab2:
    st.header("Customer Behaviour")

    customer_sales = df.groupby("CustomerID")["TotalSales"].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(customer_sales, bins=50, kde=True, ax=ax)
    ax.set_title("Distribution of Customer Sales")
    ax.set_xlabel("Total Sales per Customer")
    st.pyplot(fig)

    top_customers = customer_sales.sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_customers.values, y=top_customers.index, ax=ax)
    ax.set_title("Top 10 Customers by Sales")
    ax.set_xlabel("Sales")
    ax.set_ylabel("CustomerID")
    st.pyplot(fig)

# -------------------------------
# Tab 3: Returns Analysis
# -------------------------------
with tab3:
    st.header("Returns Analysis")

    returns = df[df["is_return"] == True]
    st.metric("Total Returns", len(returns))

    # Returns by country
    returns_country = returns.groupby("Country")["is_return"].count().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=returns_country.values, y=returns_country.index, ax=ax)
    ax.set_title("Top Countries with Returns")
    ax.set_xlabel("Number of Returns")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# -------------------------------
# Tab 4: Top Products
# -------------------------------
with tab4:
    st.header("Top Products")

    product_sales = df.groupby("Description")["TotalSales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=product_sales.values, y=product_sales.index, ax=ax)
    ax.set_title("Top 10 Products by Sales")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Product")
    st.pyplot(fig)

    st.dataframe(product_sales.reset_index().rename(columns={"Description": "Product", "TotalSales": "Sales"}))

