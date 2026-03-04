import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Smart Farming Dashboard")

# Load data
df = pd.read_csv("Smart_Farming_Crop_Yield_2024.csv")
st.subheader("Data Preview")
st.dataframe(df.head())

# ======================
# 1️⃣ Line Plot
# ======================
st.subheader("Soil Moisture & pH")

fig1, ax = plt.subplots()
ax.plot(df["soil_moisture_%"])
ax.plot(df["soil_pH"])
ax.set_xlabel("Index")
ax.set_ylabel("Value")
ax.legend(["Soil Moisture", "Soil pH"])

st.pyplot(fig1)

# ======================
# 2️⃣ Heatmap Korelasi
# ======================
st.subheader("Heatmap Korelasi")

fig2, ax2 = plt.subplots()
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax2)

st.pyplot(fig2)    
