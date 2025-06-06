import streamlit as st
import pandas as pd
from utils.db_manager import fetch_all_logs
from PIL import Image

def sidebar_and_access():
    mode = st.sidebar.selectbox("Pilih Mode Akses", ["User", "Admin"])
    return mode

def show_admin_log():
    st.subheader("📋 Log Kendaraan (Database)")

    # Ambil data dari database
    data = fetch_all_logs()
    df = pd.DataFrame(data, columns=["ID", "Plat Nomor", "Waktu Masuk", "Gambar Path"])

    # 🔍 Pencarian plat nomor
    search_plate = st.text_input("Cari Plat Nomor (misal: B1234)", "").upper()
    if search_plate:
        df = df[df["Plat Nomor"].str.contains(search_plate, case=False)]

    # 📅 Filter tanggal masuk
    start_date = st.date_input("Dari tanggal", pd.to_datetime("2024-01-01"))
    end_date = st.date_input("Sampai tanggal", pd.to_datetime("today"))

    # Konversi waktu ke datetime & filter
    df["Waktu Masuk"] = pd.to_datetime(df["Waktu Masuk"])
    df = df[(df["Waktu Masuk"].dt.date >= start_date) & (df["Waktu Masuk"].dt.date <= end_date)]

    # 📸 Tampilkan gambar thumbnail
    st.markdown("### 🖼️ Hasil Deteksi")
    for _, row in df.iterrows():
        with st.expander(f"Plat: {row['Plat Nomor']} | Masuk: {row['Waktu Masuk'].strftime('%Y-%m-%d %H:%M:%S')}"):
            st.image(row["Gambar Path"], caption=row["Gambar Path"], width=300)

    # 📊 Tampilkan tabel lengkap
    st.markdown("### 📑 Data Tabel")
    st.dataframe(df.drop(columns=["Gambar Path"]), use_container_width=True)
