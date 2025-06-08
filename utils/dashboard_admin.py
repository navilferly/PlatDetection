import streamlit as st
from utils.db_manager import get_all_logs, delete_log_by_plate_and_time, delete_all_logs
from PIL import Image
import pandas as pd  # Pastikan sudah diimpor

def sidebar_and_access():
    mode = st.sidebar.selectbox("Pilih Mode", ["Pengguna", "Admin"])
    if mode == "Admin":
        password = st.sidebar.text_input("Masukkan Password Admin", type="password")
        if password != "admin123":
            st.sidebar.error("Password salah!")
            return "Pengguna"
    return mode

def show_admin_log():
    # Baris judul + tombol Hapus Semua
    col1, col2 = st.columns([6, 2])
    with col1:
        st.header("🧾 Riwayat Tiket Parkir")
    with col2:
        if st.button("🗑️ Hapus Semua Riwayat"):
            confirm = st.checkbox("Konfirmasi hapus semua data", key="confirm_delete_all")
            if confirm:
                delete_all_logs()
                st.success("Seluruh riwayat berhasil dihapus.")
                st.experimental_rerun()
            else:
                st.warning("Centang konfirmasi terlebih dahulu untuk menghapus semua data.")

    logs = get_all_logs()
    if not logs:
        st.info("Belum ada data tiket parkir.")
        return

    df = pd.DataFrame(logs, columns=["Plat Nomor", "Waktu Masuk", "Gambar Path"])
    df = df.sort_values(by="Waktu Masuk", ascending=False)

    st.markdown("### 🖼️ Hasil Deteksi")

    for _, row in df.iterrows():
        with st.expander(f"🔹 Plat: {row['Plat Nomor']} | 🕒 {row['Waktu Masuk']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row["Gambar Path"], width=100)
            with col2:
                st.markdown(f"""
                **Plat Nomor:** `{row['Plat Nomor']}`  
                **Waktu Masuk:** `{row['Waktu Masuk']}`  
                """)
                if st.button(f"🗑️ Hapus Tiket - {row['Plat Nomor']} {row['Waktu Masuk']}", key=f"{row['Plat Nomor']}_{row['Waktu Masuk']}"):
                    delete_log_by_plate_and_time(row['Plat Nomor'], row['Waktu Masuk'])
                    st.success("Data berhasil dihapus.")
                    st.experimental_rerun()  # Refresh otomatis

    st.markdown("### 📑 Data Tabel")
    st.dataframe(df.drop(columns=["Gambar Path"]), use_container_width=True)
