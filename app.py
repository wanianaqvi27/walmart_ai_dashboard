import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG (PRO UI)
# =========================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

st.title("📊 AI Sales Analytics Dashboard")
st.markdown("Upload any sales dataset and get instant insights 🚀")

# =========================
# UPLOAD FILE
# =========================
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.success("Dataset loaded successfully ✅")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # =========================
    # AUTO DETECT COLUMNS
    # =========================
    date_candidates = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(date_candidates) == 0:
        st.warning("⚠️ No date column detected. Trend graph may not work.")
        date_col = None
    else:
        date_col = st.selectbox("Select Date Column", date_candidates)

    if len(numeric_cols) == 0:
        st.error("❌ No numeric columns found for sales analysis")
        st.stop()

    sales_col = st.selectbox("Select Sales Column", numeric_cols)

    # =========================
    # CLEAN DATA
    # =========================
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

    df = df.dropna(subset=[sales_col])

    # =========================
    # KPI METRICS
    # =========================
    total_sales = df[sales_col].sum()
    avg_sales = df[sales_col].mean()
    rows = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    col2.metric("📊 Average Sales", f"{avg_sales:,.2f}")
    col3.metric("📁 Rows", rows)

    # =========================
    # SALES TREND
    # =========================
    st.subheader("📈 Sales Trend")

    if date_col:
        try:
            monthly_sales = df.groupby(pd.Grouper(key=date_col, freq="ME"))[sales_col].sum()

            fig, ax = plt.subplots()
            monthly_sales.plot(ax=ax)
            ax.set_title("Sales Over Time")
            st.pyplot(fig)

        except:
            st.warning("⚠️ Could not generate trend graph (date issue)")
    else:
        st.info("Upload dataset with a date column for trend analysis")

    # =========================
    # TOP DATA INSIGHT
    # =========================
    st.subheader("🏆 Top 10 Highest Sales Records")

    st.dataframe(df.sort_values(by=sales_col, ascending=False).head(10))

    # =========================
    # SIMPLE INSIGHT SECTION
    # =========================
    st.subheader("📊 Quick Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Highest Sales Value:")
        st.success(df[sales_col].max())

    with col2:
        st.write("Lowest Sales Value:")
        st.warning(df[sales_col].min())

else:
    st.info("⬆️ Upload a CSV file to start analysis")
