# generate_qr.py
import qrcode
import os

def generate_qr(data, output_path='static'):
    os.makedirs(output_path, exist_ok=True)
    img = qrcode.make(data)
    qr_path = os.path.join(output_path, 'qr_code.png')
    img.save(qr_path)
    return qr_path
