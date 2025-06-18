import qrcode
import os
from PIL import Image
from utils.db_manager import get_log_by_plate

def generate_plate_qr(plate):
    # URL tujuan ketika QR di-scan
    url = f"http://localhost:8501/?plate={plate}"
    
    # Cek status keluar/menginap
    log = get_log_by_plate(plate)
    sudah_keluar = log and log[4] is not None

    # Warna QR: merah jika sudah keluar, hijau jika masih parkir
    warna_qr = "red" if sudah_keluar else "green"

    # Generate QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color=warna_qr, back_color="white").convert("RGB")

    # Simpan file QR code
    path = os.path.join("static", f"{plate}_qr.png")
    img_qr.save(path)

    return path, url
