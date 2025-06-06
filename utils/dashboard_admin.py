import streamlit as st
import pandas as pd
from utils.db_manager import fetch_all_logs

def sidebar_and_access():
    mode = st.sidebar.selectbox("Pilih Mode Akses", ["User", "Admin"])
    return mode

def show_admin_log():
    st.subheader("📋 Log Kendaraan (Database)")
    data = fetch_all_logs()
    df = pd.DataFrame(data, columns=["ID", "Plat Nomor", "Waktu Masuk", "Gambar Path"])
    st.dataframe(df, use_container_width=True)
