import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.set_page_config(page_title="Smart Farming Dashboard", layout="wide")

# 1️⃣ LOAD DATA
df = pd.read_csv("Smart_Farming_Crop_Yield_2024.csv")

st.title("🌱 Smart Farming Dashboard")

# 2️⃣ FILTER (Sidebar)
st.sidebar.header("Filter Data")

region = st.sidebar.selectbox(
    "Pilih Region",
    df["region"].unique()
)

filtered_df = df[df["region"] == region]

# 3️⃣ KPI
st.subheader("📊 Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Rata-rata Soil Moisture",
    round(filtered_df["soil_moisture_%"].mean(), 2)
)

col2.metric(
    "Rata-rata pH",
    round(filtered_df["soil_pH"].mean(), 2)
)

col3.metric(
    "Rata-rata Yield (kg/ha)",
    round(filtered_df["yield_kg_per_hectare"].mean(), 2)
)

# 4️⃣ GAUGE METER
st.subheader("🌡 Gauge Sensor Kelembaban Tanah")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=filtered_df["soil_moisture_%"].mean(),
    title={'text': "Soil Moisture (%)"},
    gauge={
        'axis': {'range': [0, 100]}
    }
))

st.plotly_chart(gauge, use_container_width=True)

# 5️⃣ GRAFIK
colA, colB = st.columns(2)

# --- Grafik Line (Time Series) ---
with colA:
    st.subheader("📈 Soil Moisture & pH")

    fig1, ax1 = plt.subplots()
    ax1.plot(filtered_df["soil_moisture_%"])
    ax1.plot(filtered_df["soil_pH"])
    ax1.set_xlabel("Index")
    ax1.set_ylabel("Value")
    ax1.legend(["Soil Moisture", "Soil pH"])

    st.pyplot(fig1)

# --- Heatmap Korelasi ---
with colB:
    st.subheader("🔥 Heatmap Korelasi")

    numeric_df = filtered_df.select_dtypes(include=["number"])

    fig2, ax2 = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax2)

    st.pyplot(fig2)

# 6️⃣ INSIGHT / ALERT
st.subheader("🤖 Insight Otomatis")

avg_moisture = filtered_df["soil_moisture_%"].mean()

if avg_moisture < 30:
    st.warning("⚠ Kelembapan tanah cenderung rendah. Perlu irigasi tambahan.")
else:
    st.success("✅ Kelembapan tanah dalam kondisi optimal.")
