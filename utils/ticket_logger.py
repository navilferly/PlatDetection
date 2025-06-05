def save_log_and_ticket(plate, waktu_masuk, processed_path):
    import os
    log_path = "detection_log.csv"
    with open(log_path, "a") as log:
        log.write(f"{waktu_masuk},{plate}\n")

    ticket_html = f"""
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
    """
    return ticket_html
