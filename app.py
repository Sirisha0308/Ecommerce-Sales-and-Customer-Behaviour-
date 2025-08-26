import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-commerce Sales & Customer Behaviour Analysis", layout="wide")

# ------------------------------
# Load dataset
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data_updated.csv", encoding="ISO-8859-1", low_memory=False)
    return df

df = load_data()

# ------------------------------
# Data Cleaning
# ------------------------------
df["is_return"] = df["Quantity"] < 0
df = df[df["UnitPrice"] > 0]
df = df.dropna(subset=["Description", "CustomerID"])
df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# ✅ Create TotalSales for all sections
df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to", 
    ["Dataset Overview", "Missing Values", "Top Products", "Top Countries", "Monthly Trends", "Customer Analysis", "RFM Analysis"]
)

# ------------------------------
# Sections
# ------------------------------
if section == "Dataset Overview":
    st.title("📊 Dataset Overview")
    st.write(df.head(20))
    st.write("Shape:", df.shape)
    st.write(df.describe())
    st.write("Data Types:")
    st.write(df.dtypes)

elif section == "Missing Values":
    st.title("🚫 Missing Values")
    st.write(df.isnull().sum())

elif section == "Top Products":
    st.title("🏆 Top 10 Most Sold Products")
    top_products = df["Description"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_products.values, y=top_products.index, ax=ax, palette="viridis")
    st.pyplot(fig)

elif section == "Top Countries":
    st.title("🌍 Top 10 Countries by Sales")
    country_sales = df.groupby("Country")["Quantity"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=country_sales.values, y=country_sales.index, ax=ax, palette="coolwarm")
    st.pyplot(fig)

elif section == "Monthly Trends":
    st.title("📈 Monthly Sales Trend")
    monthly_sales = df.groupby(df["InvoiceDate"].dt.to_period("M"))["Quantity"].sum()
    fig, ax = plt.subplots(figsize=(12, 5))
    monthly_sales.plot(ax=ax, marker="o")
    st.pyplot(fig)

elif section == "Customer Analysis":
    st.title("👥 Customer Analysis")
    
    # Top Customers by Sales
    st.subheader("Top 10 Customers by Total Sales")
    df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
    top_customers = df.groupby("CustomerID")["TotalSales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_customers.values, y=top_customers.index, ax=ax, palette="magma")
    st.pyplot(fig)

elif section == "RFM Analysis":
    st.title("📌 RFM (Recency, Frequency, Monetary) Analysis")
    
    import datetime as dt
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "count",
        "TotalSales": "sum"
    })
    rfm.rename(columns={
        "InvoiceDate": "Recency",
        "InvoiceNo": "Frequency",
        "TotalSales": "Monetary"
    }, inplace=True)

    st.write(rfm.describe())

    # Recency Distribution
    st.subheader("Recency Distribution")
    fig, ax = plt.subplots()
    sns.histplot(rfm["Recency"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

    # Frequency Distribution
    st.subheader("Frequency Distribution")
    fig, ax = plt.subplots()
    sns.histplot(rfm["Frequency"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

    # Monetary Distribution
    st.subheader("Monetary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(rfm["Monetary"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)
