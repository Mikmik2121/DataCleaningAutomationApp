import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Order Cleaner", layout="wide")

st.title("📊 Raw Data Cleaning Automation")

# Upload file
uploaded_file = st.file_uploader(
    "Upload your raw file (.xlsx or .csv)",
    type=["xlsx", "csv"]
)

# Detect platform
def detect_platform(filename):
    name = filename.upper()
    if "LAZADA" in name:
        return "lazada"
    elif "SHOPEE" in name:
        return "shopee"
    elif "ZALORA" in name:
        return "zalora"
    elif "SHOPIFY" in name:
        return "shopify"
    elif "TIKTOK" in name:
        return "tiktok"
    return None


# ===== CLEANING FUNCTIONS (simplified versions of yours) ===== #

def clean_lazada(df):
    df['createTime'] = pd.to_datetime(df['createTime'], errors='coerce')
    df = df.sort_values(by='createTime')
    return df

def clean_shopee(df):
    df['Order Creation Date'] = pd.to_datetime(df['Order Creation Date'], errors='coerce')
    df = df.sort_values(by='Order Creation Date')
    return df

def clean_zalora(df):
    df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')
    df = df.sort_values(by='Created at')
    return df

def clean_shopify(df):
    df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')
    df = df.sort_values(by='Created at')
    return df

def clean_tiktok(df):
    df['Created Time'] = pd.to_datetime(df['Created Time'], errors='coerce')
    df = df.sort_values(by='Created Time')
    return df


# ===== MAIN LOGIC ===== #

if uploaded_file:
    platform = detect_platform(uploaded_file.name)

    if platform is None:
        st.error("❌ Could not detect platform from filename.")
    else:
        st.success(f"Detected platform: {platform.upper()}")

        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Clean
        if platform == "lazada":
            df_clean = clean_lazada(df)
        elif platform == "shopee":
            df_clean = clean_shopee(df)
        elif platform == "zalora":
            df_clean = clean_zalora(df)
        elif platform == "shopify":
            df_clean = clean_shopify(df)
        elif platform == "tiktok":
            df_clean = clean_tiktok(df)

        st.subheader("Preview (Cleaned Data)")
        st.dataframe(df_clean.head(50))

        # Convert to Excel in memory
        output = io.BytesIO()
        df_clean.to_excel(output, index=False)
        output.seek(0)

        st.download_button(
            label="⬇️ Download Cleaned File",
            data=output,
            file_name=f"{platform}_cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
