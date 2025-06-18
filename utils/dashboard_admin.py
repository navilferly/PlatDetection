import streamlit as st
from utils.db_manager import get_all_logs
import pandas as pd

# Sidebar: pilih mode (Admin/Pengguna) dengan password untuk admin
def sidebar_and_access():
    mode = st.sidebar.selectbox("Pilih Mode", ["Pengguna", "Admin"])
    if mode == "Admin":
        password = st.sidebar.text_input("Masukkan Password Admin", type="password")
        if password != "admin123":
            st.sidebar.error("Password salah!")
            return "Pengguna"
    return mode

# Menampilkan tabel data parkir untuk admin
def show_admin_log():
    st.markdown("### 📊 Laporan Data Parkir")

    logs = get_all_logs()
    if not logs:
        st.info("Belum ada data kendaraan masuk.")
        return

    try:
        # Cek jumlah kolom dan sesuaikan nama kolom
        if len(logs[0]) == 4:
            df = pd.DataFrame(logs, columns=["ID", "Plat Nomor", "Waktu Masuk", "Gambar Path"])
        elif len(logs[0]) == 6:
            df = pd.DataFrame(logs, columns=["ID", "Plat Nomor", "Waktu Masuk", "Gambar Path", "Waktu Keluar", "Biaya"])
        else:
            st.error(f"Struktur data dari database tidak sesuai. Jumlah kolom: {len(logs[0])}")
            return
    except Exception as e:
        st.error(f"Gagal memproses data: {e}")
        return

    # Tampilkan tabel tanpa kolom gambar (supaya rapi)
    if "Gambar Path" in df.columns:
        df_display = df.drop(columns=["Gambar Path"])
    else:
        df_display = df

    st.dataframe(df_display, use_container_width=True)

    # Tombol download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="laporan_parkir.csv",
        key="download_laporan_csv"
    )
