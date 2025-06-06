import streamlit as st
import os
import requests
import pandas as pd
from datetime import datetime

from utils.db_manager import init_db, insert_log_to_db
from utils.upload_input import upload_and_save_image
from utils.detect_draw import draw_detection_on_image
from utils.qr_generator import generate_plate_qr
from utils.ticket_logger import save_log_and_ticket
from utils.dashboard_admin import sidebar_and_access, show_admin_log

# Konfigurasi API
API_TOKEN = 'Token 38feacaf631d8bfa6a98bc34f119da7cebee0c64'
API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Inisialisasi Database
init_db()

# Setup halaman
st.set_page_config(page_title="Tiket Parkir Otomatis", layout="centered")
st.title("🎟️ Tiket Parkir Otomatis")

# Mode akses
mode = sidebar_and_access()

# Mode hasil scan QR
query_params = st.query_params
if "plate" in query_params:
    plate_from_qr = query_params["plate"][0].upper()
    waktu_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.success("✅ QR berhasil dipindai!")
    st.markdown(f"""
    ### 🔍 Hasil Scan QR
    - **Plat Nomor:** `{plate_from_qr}`
    - **Waktu Scan:** {waktu_scan}
    """)
    st.stop()

# Upload gambar
uploaded_file = st.file_uploader("Upload gambar plat nomor kendaraan", type=["jpg", "jpeg", "png"])
if uploaded_file:
    file_path = upload_and_save_image(uploaded_file)

    with st.spinner("🔍 Memproses gambar..."):
        with open(file_path, 'rb') as img:
            response = requests.post(
                API_URL,
                files=dict(upload=img),
                headers={'Authorization': API_TOKEN}
            )

        if response.status_code in [200, 201]:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Deteksi dan anotasi
                image_result, plate = draw_detection_on_image(file_path, result)
                processed_filename = f"{plate}.png"
                processed_path = os.path.join("static", processed_filename)
                image_result.save(processed_path)

                # Generate QR
                qr_path, full_url = generate_plate_qr(plate)

                # Simpan log ke CSV
                ticket_html = save_log_and_ticket(plate, waktu_masuk, processed_path)

                # Simpan log ke database
                insert_log_to_db(plate, waktu_masuk, processed_path)

                # Tampilkan hasil
                st.success("✅ Plat nomor berhasil terdeteksi")
                col1, col2 = st.columns(2)
                col1.image(file_path, caption="📷 Gambar Asli", use_container_width=True)
                col2.image(processed_path, caption="📍 Gambar dengan Deteksi", use_container_width=True)
                st.image(qr_path, caption="📎 QR Code (Scan untuk lihat hasil)", use_container_width=False)

                st.markdown(ticket_html, unsafe_allow_html=True)

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

# Hanya admin yang bisa lihat log
if mode == "Admin":
    show_admin_log()
