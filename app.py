import streamlit as st
import os
import requests
import pandas as pd
from datetime import datetime

from utils.db_manager import (
    init_db, insert_log_to_db, get_log_by_plate,
    get_all_logs, update_log_exit
)
from utils.upload_input import upload_and_save_image
from utils.detect_draw import draw_detection_on_image
from utils.qr_generator import generate_plate_qr
from utils.dashboard_admin import sidebar_and_access, show_admin_log
from utils.ticket_logger import generate_ticket_text

API_TOKEN = 'Token 38feacaf631d8bfa6a98bc34f119da7cebee0c64'
API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Inisialisasi DB
init_db()

st.set_page_config(page_title="Tiket Parkir Otomatis", layout="centered")
st.title("🎟️ Tiket Parkir")

# Akses mode: Pengguna / Admin
mode = sidebar_and_access()

# === HANDLE SCAN QR (opsional) ===
query_params = st.query_params
if "plate" in query_params and not st.session_state.get("qr_scanned", False):
    plate_from_qr = query_params["plate"][0].upper()
    waktu_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state["qr_scanned"] = True
    st.success("✅ QR berhasil dipindai!")
    st.subheader("🔍 Hasil Scan QR")
    st.text(f"🚗 Plat Nomor : {plate_from_qr}")
    st.text(f"⏰ Waktu Scan : {waktu_scan}")
    st.stop()

# === FITUR UNTUK PENGGUNA ===
if mode == "Pengguna":
    st.subheader("📷 Upload Gambar Plat Nomor")
    uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        if st.session_state.get("last_processed") == uploaded_file.name:
            st.info("✅ Gambar ini sudah diproses sebelumnya.")
            st.stop()
        else:
            st.session_state["last_processed"] = uploaded_file.name

        file_path = upload_and_save_image(uploaded_file)

        with st.spinner("🔍 Memproses gambar..."):
            try:
                with open(file_path, 'rb') as img:
                    response = requests.post(
                        API_URL,
                        files=dict(upload=img),
                        headers={'Authorization': API_TOKEN},
                        timeout=10
                    )
            except requests.exceptions.RequestException as e:
                st.error(f"Gagal menghubungi API: {e}")
                st.stop()

        if response.status_code in [200, 201]:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                plate = result["plate"].upper()
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                image_result, _ = draw_detection_on_image(file_path, result)
                processed_path = os.path.join("static", f"{plate}.png")
                image_result.save(processed_path)

                insert_log_to_db(plate, waktu, processed_path)

                qr_path, full_url = generate_plate_qr(plate)

                st.success("✅ Plat nomor berhasil terdeteksi dan disimpan!")

                st.subheader("📸 Hasil Deteksi")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(file_path, caption="Gambar Asli", use_container_width=True)
                with col2:
                    st.image(processed_path, caption="Gambar dengan Deteksi", use_container_width=True)

                st.subheader("📎 QR Code")
                st.image(qr_path, caption="Scan untuk buka data kendaraan")

                st.subheader("🎫 Tiket Parkir")
                ticket_text = generate_ticket_text(plate, waktu)
                st.text(ticket_text)

                with open(processed_path, "rb") as img_file:
                    st.download_button(
                        label="📥 Unduh Gambar Hasil",
                        data=img_file,
                        file_name=f"{plate}.png",
                        mime="image/png"
                    )
            else:
                st.warning("⚠️ Tidak ada plat nomor yang terdeteksi.")
        else:
            st.error(f"Gagal request: {response.status_code}\n{response.text}")

# === FITUR UNTUK ADMIN ===
if mode == "Admin":
    st.write("---")
    st.subheader("🛑 Kendaraan Keluar")
    plate_out = st.text_input("No Polisi Keluar")
    if st.button("🧾 Hitung Biaya"):
        try:
            log = get_log_by_plate(plate_out.upper())
            if log:
                waktu_masuk = datetime.strptime(log[2], "%Y-%m-%d %H:%M:%S")
                waktu_keluar = datetime.now()
                durasi = waktu_keluar - waktu_masuk
                durasi_menit = durasi.total_seconds() / 60

                if durasi_menit <= 10:
                    biaya = 300000
                elif durasi_menit <= 60:
                    biaya = 350000
                else:
                    biaya = 500000

                st.success("✅ Data ditemukan!")
                st.write(f"🕒 Waktu Masuk: {waktu_masuk}")
                st.write(f"🕒 Waktu Keluar: {waktu_keluar}")
                st.write(f"⏳ Durasi: {durasi}")
                st.write(f"💰 Biaya Parkir: Rp {biaya:,.0f}")

                update_log_exit(plate_out.upper(), waktu_keluar.strftime("%Y-%m-%d %H:%M:%S"), biaya)

                qr_path, full_url = generate_plate_qr(plate_out.upper())
                st.subheader("📎 QR Code (Setelah Kendaraan Keluar)")
                st.image(qr_path, caption="QR berwarna merah jika kendaraan sudah keluar")
            else:
                st.warning("❌ Data kendaraan tidak ditemukan.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

    show_admin_log()
