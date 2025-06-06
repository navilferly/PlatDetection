import os
import pandas as pd
import streamlit as st

def sidebar_and_access():
    st.sidebar.markdown("## 🔐 Mode Akses")
    mode = st.sidebar.radio("Pilih Mode:", ["User", "Admin"])
    if mode == "Admin":
        password = st.sidebar.text_input("Masukkan Password Admin", type="password")
        if password != "admin123":
            st.sidebar.warning("🔒 Akses Admin Dikunci.")
            st.stop()
        else:
            st.sidebar.success("✅ Akses Admin Diaktifkan")
    return mode

def show_admin_log():
    if os.path.exists("detection_log.csv"):
        df_log = pd.read_csv("detection_log.csv", names=["Waktu", "Plat"])
        st.markdown("### 🕘 Riwayat Deteksi")
        st.dataframe(df_log[::-1], use_container_width=True)
    else:
        st.info("Belum ada data deteksi yang tersimpan.")
