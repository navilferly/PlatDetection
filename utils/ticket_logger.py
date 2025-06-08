def generate_ticket_html(plate, waktu_masuk, image_path):
    return f"""
    ### 🎫 Tiket Parkir
    - 🚗 **Plat Nomor:** `{plate}`
    - ⏰ **Waktu Masuk:** {waktu_masuk}
    """
