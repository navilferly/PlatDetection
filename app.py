import streamlit as st
import os
import requests
import pandas as pd
from datetime import datetime

# Import modul internal
from utils.db_manager import init_db, insert_log_to_db
from utils.upload_input import upload_and_save_image
from utils.detect_draw import draw_detection_on_image
from utils.qr_generator import generate_plate_qr
from utils.ticket_logger import generate_ticket_html
from utils.dashboard_admin import sidebar_and_access, show_admin_log

# Konfigurasi API
API_TOKEN = 'Token 38feacaf631d8bfa6a98bc34f119da7cebee0c64'
API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Inisialisasi Database
init_db()

# Konfigurasi Halaman
st.set_page_config(page_title="Tiket Parkir Otomatis", layout="centered")
st.title("🎟️ Tiket Parkir Otomatis")

# Sidebar Akses
mode = sidebar_and_access()

# Handle QR Scan via URL Query
query_params = st.query_params
if "plate" in query_params:
    plate_from_qr = query_params["plate"][0].upper()
    waktu_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success("✅ QR berhasil dipindai!")
    st.subheader("🔍 Hasil Scan QR")
    st.text(f"🚗 Plat Nomor : {plate_from_qr}")
    st.text(f"⏰ Waktu Scan : {waktu_scan}")
    st.stop()

# Upload dan Deteksi Plat Nomor
st.subheader("📷 Upload Gambar Plat Nomor")
uploaded_file = st.file_uploader("Pilih gambar", type=["jpg", "jpeg", "png"])

if uploaded_file:
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
                waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                image_result, plate = draw_detection_on_image(file_path, result)
                if not plate:
                    st.warning("⚠️ Plat nomor tidak terdeteksi.")
                    st.stop()

                processed_filename = f"{plate}.png"
                processed_path = os.path.join("static", processed_filename)
                image_result.save(processed_path)

                qr_path, full_url = generate_plate_qr(plate)
                insert_log_to_db(plate, waktu_masuk, processed_path)
                ticket_html = generate_ticket_html(plate, waktu_masuk, processed_path)

                st.success("✅ Plat nomor berhasil terdeteksi")

                # Tampilkan hasil deteksi
                st.subheader("📸 Hasil Deteksi")
                col1, col2 = st.columns(2)
                with col1:
                    st.image(file_path, caption="Gambar Asli", use_container_width=True)
                with col2:
                    st.image(processed_path, caption="Gambar dengan Deteksi", use_container_width=True)

                # QR Code dan Tiket
                st.subheader("📎 QR Code")
                st.image(qr_path, caption="Scan untuk buka tiket")
                st.markdown(ticket_html, unsafe_allow_html=True)

                # Tombol Unduh Gambar
                with open(processed_path, "rb") as img_file:
                    st.download_button(
                        label="📥 Unduh Gambar Hasil",
                        data=img_file,
                        file_name=processed_filename,
                        mime="image/png"
                    )
            else:
                st.warning("⚠️ Tidak ada plat nomor yang terdeteksi.")
        else:
            st.error(f"Gagal request: {response.status_code}\n{response.text}")

# Mode Admin
if mode == "Admin":
    show_admin_log()
