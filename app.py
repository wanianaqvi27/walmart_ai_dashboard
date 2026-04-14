import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# =====================
# PAGE CONFIG (PRO LOOK)
# =====================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

# =====================
# HEADER
# =====================
st.title("📊 AI Sales Forecast Dashboard")
st.markdown("Upload Walmart data and get instant AI insights + predictions")

# =====================
# SIDEBAR
# =====================
st.sidebar.header("⚙️ Controls")

file = st.sidebar.file_uploader("Upload Dataset", type=["csv"])

# =====================
# MAIN APP
# =====================
if file:
    df = pd.read_csv(file)

    st.success("Data loaded successfully ✅")

    # FIX DATE
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    # =====================
    # KPI CARDS (PRO LOOK)
    # =====================
    total_sales = df["Weekly_Sales"].sum()
    avg_sales = df["Weekly_Sales"].mean()
    total_stores = df["Store"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    col2.metric("📊 Avg Sales", f"{avg_sales:,.0f}")
    col3.metric("🏬 Stores", total_stores)

    # =====================
    # CHARTS SECTION
    # =====================
    st.subheader("📈 Sales Trend")

    fig, ax = plt.subplots()
    df.groupby("Date")["Weekly_Sales"].sum().plot(ax=ax)
    st.pyplot(fig)

    # =====================
    # INSIGHTS SECTION
    # =====================
    st.subheader("🏆 Top Stores")
    st.write(df.groupby("Store")["Weekly_Sales"].sum().sort_values(ascending=False).head(10))

    st.subheader("🏖️ Holiday Impact")
    st.write(df.groupby("Holiday_Flag")["Weekly_Sales"].mean())

    # =====================
    # ML MODEL
    # =====================
    st.subheader("🤖 AI Prediction Model")

    features = ["Store", "Holiday_Flag", "Year", "Month"]

    X = df[features]
    y = df["Weekly_Sales"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    # =====================
    # PREDICTION UI (PRO)
    # =====================
    st.subheader("🔮 Predict Sales")

    col1, col2, col3, col4 = st.columns(4)

    store = col1.number_input("Store", 1, 50, 1)
    holiday = col2.selectbox("Holiday", [0, 1])
    year = col3.number_input("Year", 2010, 2030, 2015)
    month = col4.number_input("Month", 1, 12, 1)

    if st.button("Predict Now 🚀"):
        prediction = model.predict([[store, holiday, year, month]])
        st.success(f"Predicted Weekly Sales: ${prediction[0]:,.2f}")
