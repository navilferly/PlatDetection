import streamlit as st
import os
import requests
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from generate_qr import generate_qr
from datetime import datetime
from urllib.parse import urlencode

# Konfigurasi API
API_TOKEN = 'Token 38feacaf631d8bfa6a98bc34f119da7cebee0c64'
API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'

# Setup halaman
st.set_page_config(page_title="Tiket Parkir Otomatis", layout="centered")
st.title("🎟️ Tiket Parkir Otomatis")

# Sidebar Navigasi dan Branding
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/17/Plate_Recognizer_logo.png", width=100)
    st.markdown("## 📂 Navigasi")
    st.markdown("- [Halaman Utama](#)")
    st.markdown("- [API Source](https://platerecognizer.com)")

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
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    log_path = "detection_log.csv"

    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("🔍 Memproses gambar..."):
        with open(file_path, 'rb') as img:
            response = requests.post(
                API_URL,
                files=dict(upload=img),
                headers={'Authorization': API_TOKEN}
            )

        if response.status_code not in [200, 201]:
            st.error(f"Gagal request: {response.status_code}\n{response.text}")
        else:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                plate = result["plate"].upper()
                box = result["box"]
                waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                image = Image.open(file_path)
                draw = ImageDraw.Draw(image)

                # Kotak deteksi
                draw.rectangle(
                    [(box["xmin"], box["ymin"]), (box["xmax"], box["ymax"])],
                    outline="red", width=4
                )

                # Font dan ukuran teks besar dengan outline
                try:
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
                    font = ImageFont.truetype(font_path, 150)
                except:
                    font = ImageFont.load_default()

                text_bbox = draw.textbbox((0, 0), plate, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                box_center_x = (box["xmin"] + box["xmax"]) // 2
                text_x = box_center_x - text_width // 2
                text_y = box["ymin"] - text_height - 10
                if text_y < 0:
                    text_y = box["ymin"] + 10

                for ox in range(-2, 3):
                    for oy in range(-2, 3):
                        if ox != 0 or oy != 0:
                            draw.text((text_x + ox, text_y + oy), plate, fill="black", font=font)
                draw.text((text_x, text_y), plate, fill="red", font=font)

                processed_filename = f"{plate}.png"
                processed_path = os.path.join("static", processed_filename)
                image.save(processed_path)

                base_url = "http://localhost:8501/"
                full_url = f"{base_url}?" + urlencode({"plate": plate})
                qr_path = generate_qr(full_url)

                # Simpan log deteksi
                with open(log_path, "a") as log:
                    log.write(f"{waktu_masuk},{plate}\n")

                # Tampilkan hasil
                st.success("✅ Plat nomor berhasil terdeteksi")
                col1, col2 = st.columns(2)
                col1.image(file_path, caption="📷 Gambar Asli", use_container_width=True)
                col2.image(processed_path, caption="📍 Gambar dengan Deteksi", use_container_width=True)

                st.image(qr_path, caption="📎 QR Code (Scan untuk lihat hasil)", use_container_width=False)

                # Tiket Parkir & Statistik
                st.markdown("---")
                col3, col4 = st.columns(2)
                col3.metric("Plat Nomor", plate)
                col4.metric("Waktu Masuk", waktu_masuk)

                st.markdown("### 🎫 Tiket Parkir Kendaraan")
                st.markdown(f"""
                <style>
                .tiket {{
                    background-color: #f5f5f5;
                    border: 2px dashed #999;
                    padding: 20px;
                    border-radius: 10px;
                    font-family: monospace;
                }}
                </style>
                <div class='tiket'>
                🅿️ <b>Plat Nomor :</b> {plate}<br>
                🕒 <b>Waktu Masuk :</b> {waktu_masuk}<br>
                </div>
                """, unsafe_allow_html=True)

                with open(processed_path, "rb") as img_file:
                    st.download_button(
                        label="📥 Unduh Gambar Hasil",
                        data=img_file,
                        file_name=processed_filename,
                        mime="image/png"
                    )
            else:
                st.warning("⚠️ Tidak ada plat nomor yang terdeteksi.")

# Tampilkan Riwayat
st.markdown("---")
st.markdown("### 🕘 Riwayat Deteksi")
if os.path.exists("detection_log.csv"):
    df_log = pd.read_csv("detection_log.csv", names=["Waktu", "Plat"])
    st.dataframe(df_log[::-1], use_container_width=True)
