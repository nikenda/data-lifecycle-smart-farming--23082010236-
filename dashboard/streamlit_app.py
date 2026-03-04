import streamlit as st
import pandas as pd

st.title("Smart Farming Dashboard")

st.write("Aplikasi berhasil jalan!")

# contoh kalau ada data
try:
    df = pd.read_csv("data/smart_farming.csv")  # sesuaikan nama file kamu
    st.success("Data berhasil dibaca")
    st.dataframe(df.head())
except:
    st.warning("Data belum ditemukan")
