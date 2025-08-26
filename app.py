import streamlit as st
import pandas as pd
import zipfile
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="E-commerce Sales & Customer Behaviour Analysis",
    layout="wide"
)

# -------------------------------
# Load Dataset from ZIP
# -------------------------------
@st.cache_data
def load_data():
    zip_path = "cleaned_data_updated.zip"   # ensure this is in GitHub repo

    with zipfile.ZipFile(zip_path, 'r') as z:
        file_name = z.namelist()[0]  # first file inside zip
        with z.open(file_name) as f:
            df = pd.read_csv(f, encoding="ISO-8859-1", low_memory=False)

    # Basic cleaning
    if "Quantity" in df.columns:
        df["is_return"] = df["Quantity"] < 0
    if "UnitPrice" in df.columns:
        df = df[df["UnitPrice"] > 0]
    if "Description" in df.columns and "CustomerID" in df.columns:
        df = df.dropna(subset=["Description", "CustomerID"])
    if "CustomerID" in df.columns:
        df["CustomerID"] = df["CustomerID"].astype(str)  # keep as string
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    return df

df = load_data()

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.title("📊 E-commerce Sales & Customer Behaviour Analysis")

# Dataset Preview
st.subheader("🔍 Dataset Preview")
st.write(df.head())

# Dataset Info
st.subheader("📌 Dataset Information")
st.write("Shape of dataset:", df.shape)
st.write("Columns:", df.columns.tolist())

# -------------------------------
# Example Visualizations
# -------------------------------
st.subheader("📈 Sales by Country")
if "Country" in df.columns and "Sales" in df.columns:
    country_sales = df.groupby("Country")["Sales"].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=country_sales.values, y=country_sales.index, ax=ax, palette="viridis")
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Country")
    ax.set_title("Top 10 Countries by Sales")
    st.pyplot(fig)
else:
    st.warning("⚠️ Columns `Country` and `Sales` not found in dataset.")

st.subheader("👥 Top 10 Customers by Sales")
if "CustomerID" in df.columns and "Sales" in df.columns:
    top_customers = df.groupby("CustomerID")["Sales"].sum().nlargest(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_customers.values, y=top_customers.index, ax=ax, palette="magma")
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("Customer ID")
    ax.set_title("Top 10 Customers by Sales")
    st.pyplot(fig)
else:
    st.warning("⚠️ Columns `CustomerID` and `Sales` not found in dataset.")

st.subheader("🕒 Sales Over Time")
if "InvoiceDate" in df.columns and "Sales" in df.columns:
    sales_over_time = df.groupby(df["InvoiceDate"].dt.to_period("M"))["Sales"].sum()

    fig, ax = plt.subplots(figsize=(12, 5))
    sales_over_time.plot(ax=ax, marker="o")
    ax.set_ylabel("Total Sales")
    ax.set_xlabel("Date")
    ax.set_title("Sales Over Time (Monthly)")
    st.pyplot(fig)
else:
    st.warning("⚠️ Columns `InvoiceDate` and `Sales` not found in dataset.")
