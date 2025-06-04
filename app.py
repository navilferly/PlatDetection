import cv2
import os
import requests
from utils.ocr import extract_text_from_plate
from utils.generate_qr import generate_qr_code

# === KONFIGURASI ===
USE_API = True  # True: pakai PlateRecognizer API, False: pakai Haar Cascade
API_TOKEN = "GANTI_DENGAN_TOKEN_MU"  # ⚠️ Ganti token dengan milikmu

# === FUNGSI UNTUK DETEKSI MENGGUNAKAN API ===
def detect_plate_with_api(image_path, api_token):
    url = "https://api.platerecognizer.com/v1/plate-reader/"
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            url,
            files={"upload": image_file},
            headers={"Authorization": f"Token {api_token}"}
        )
    if response.status_code == 200:
        data = response.json()
        try:
            return data['results'][0]['plate'].upper()
        except (IndexError, KeyError):
            return None
    else:
        print("API Error:", response.status_code, response.text)
        return None

# === PROSES UTAMA ===
image_path = 'samples/contoh_plat.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Gagal memuat gambar. Periksa path:", image_path)
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

if USE_API:
    # --- Deteksi via API ---
    text = detect_plate_with_api(image_path, API_TOKEN)
    if text:
        print("Teks Plat (API):", text)
        generate_qr_code(text)
        cv2.putText(image, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    else:
        print("Plat tidak terdeteksi via API.")
else:
    # --- Deteksi via Haar Cascade + Tesseract ---
    cascade_path = 'models/haarcascade_russian_plate_number.xml'
    plate_cascade = cv2.CascadeClassifier(cascade_path)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    if len(plates) == 0:
        print("Tidak ada plat terdeteksi.")
    for (x, y, w, h) in plates:
        plate_img = image[y:y+h, x:x+w]
        text = extract_text_from_plate(plate_img)
        print("Teks Plat:", text)
        generate_qr_code(text)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

# === TAMPILKAN HASIL ===
cv2.imshow('Hasil Deteksi Plat', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
