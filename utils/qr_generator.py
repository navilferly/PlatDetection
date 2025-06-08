import qrcode
import os

def generate_plate_qr(plate, output_path='static'):
    os.makedirs(output_path, exist_ok=True)
    full_url = f"http://192.168.4.109/?plate={plate}"
    img = qrcode.make(full_url)
    qr_path = os.path.join(output_path, f'{plate}_qr.png')
    img.save(qr_path)
    return qr_path, full_url
