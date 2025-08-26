import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

# Load dataset
@st.cache_data
def load_data():
    with zipfile.ZipFile("cleaned_dataset_updated.zip", "r") as z:
        with z.open("cleaned_dataset_updated.csv") as f:
            df = pd.read_csv(f)
    return df

df = load_data()

st.title("📊 E-commerce Sales & Customer Behavior Dashboard")

# Show dataset
if st.checkbox("Show raw data"):
    st.write(df.head())
    st.write("Columns:", df.columns.tolist())

# --- Sales by Country ---
st.subheader("🌍 Sales by Country")
if "Country" in df.columns and "TotalPrice" in df.columns:
    sales_by_country = df.groupby("Country")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=sales_by_country.sort_values("TotalPrice", ascending=False).head(10),
                x="TotalPrice", y="Country", ax=ax)
    ax.set_title("Top 10 Countries by Sales")
    st.pyplot(fig)
else:
    st.warning("Columns Country and TotalPrice not found in dataset.")

# --- Top 10 Customers by Sales ---
st.subheader("👥 Top 10 Customers by Sales")
if "CustomerID" in df.columns and "TotalPrice" in df.columns:
    top_customers = df.groupby("CustomerID")["TotalPrice"].sum().reset_index().sort_values(by="TotalPrice", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_customers, x="TotalPrice", y="CustomerID", ax=ax)
    ax.set_title("Top 10 Customers by Sales")
    st.pyplot(fig)
else:
    st.warning("Columns CustomerID and TotalPrice not found in dataset.")

# --- Sales Over Time ---
st.subheader("⏰ Sales Over Time")
if "InvoiceDate" in df.columns and "TotalPrice" in df.columns:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    sales_time = df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"].sum().reset_index()
    sales_time["InvoiceDate"] = sales_time["InvoiceDate"].astype(str)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=sales_time, x="InvoiceDate", y="TotalPrice", marker="o", ax=ax)
    ax.set_title("Monthly Sales Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("Columns InvoiceDate and TotalPrice not found in dataset.")
