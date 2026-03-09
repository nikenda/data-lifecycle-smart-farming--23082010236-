import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Smart Farming Dashboard", layout="wide")

# 1️⃣ LOAD DATA
df = pd.read_csv("Smart_Farming_Crop_Yield_2024.csv")

st.title("🌱 Smart Farming Dashboard")

# 2️⃣ FILTER DATA (SIDEBAR)
st.sidebar.header("Filter Data")

region = st.sidebar.selectbox(
    "Pilih Region",
    df["region"].unique()
)

filtered_df = df[df["region"] == region]

# 3️⃣ QUERY DATA SESUAI PERMINTAAN
data_query = filtered_df[['soil_moisture_%', 'temperature_C', 'humidity_%', 'soil_pH', 'yield_kg_per_hectare']]

# nilai kelembaban terakhir
kelembaban_sekarang = data_query['soil_moisture_%'].iloc[-1]

# korelasi antar variabel
korelasi_data = data_query.corr()

# 4️⃣ KPI
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

# 5️⃣ GAUGE SENSOR KELEMBABAN
st.subheader("🌡 Gauge Sensor Kelembaban Tanah")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=kelembaban_sekarang,
    title={'text': "Soil Moisture (%)"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, 30], 'color': "red"},
            {'range': [30, 60], 'color': "yellow"},
            {'range': [60, 100], 'color': "lightgreen"}
        ]
    }
))

st.plotly_chart(gauge, use_container_width=True)

# 6️⃣ GRAFIK
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

    fig2, ax2 = plt.subplots()
    sns.heatmap(korelasi_data, annot=True, cmap="coolwarm", ax=ax2)

    st.pyplot(fig2)

# 7️⃣ INSIGHT OTOMATIS
st.subheader("🤖 Insight Otomatis")

avg_moisture = filtered_df["soil_moisture_%"].mean()

if avg_moisture < 30:
    st.warning("⚠ Kelembapan tanah cenderung rendah. Perlu irigasi tambahan.")
else:
    st.success("✅ Kelembapan tanah dalam kondisi optimal.")
