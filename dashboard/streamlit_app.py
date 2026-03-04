import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# 1️⃣ LOAD DATA
# =====================
df = pd.read_csv("Smart_Farming_Crop_Yield_2024.csv")

st.title("Smart Farming Dashboard")

# =====================
# 2️⃣ FILTER (Sidebar)
# =====================
st.sidebar.header("Filter Data")

region = st.sidebar.selectbox(
    "Pilih Region",
    df["region"].unique()
)

filtered_df = df[df["region"] == region]

# =====================
# 3️⃣ KPI
# =====================
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

col1.metric("Rata-rata Soil Moisture",
            round(filtered_df["soil_moisture_%"].mean(), 2))

col2.metric("Rata-rata pH",
            round(filtered_df["soil_pH"].mean(), 2))

col3.metric("Rata-rata Yield",
            round(filtered_df["yield_kg_per_hectare"].mean(), 2))

# =====================
# 4️⃣ GRAFIK
# =====================
fig1, ax1 = plt.subplots()
ax1.plot(filtered_df["soil_moisture_%"])
ax1.plot(filtered_df["soil_pH"])
ax1.legend(["Soil Moisture", "Soil pH"])

# Heatmap hanya numerik
numeric_df = filtered_df.select_dtypes(include=["number"])

fig2, ax2 = plt.subplots()
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax2)

colA, colB = st.columns(2)

with colA:
    st.pyplot(fig1)

with colB:
    st.pyplot(fig2)

# =====================
# 5️⃣ INSIGHT
# =====================
st.subheader("Insight Otomatis")

if filtered_df["soil_moisture_%"].mean() < 30:
    st.warning("⚠ Kelembapan tanah cenderung rendah.")
else:
    st.success("✅ Kelembapan tanah dalam kondisi optimal.")
