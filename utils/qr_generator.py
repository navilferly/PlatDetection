def generate_plate_qr(plate):
    from generate_qr import generate_qr
    from urllib.parse import urlencode
    base_url = "http://localhost:8501/"
    full_url = f"{base_url}?" + urlencode({"plate": plate})
    qr_path = generate_qr(full_url)
    return qr_path, full_url