import sqlite3
import os

DB_PATH = "parking_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT,
            waktu_masuk TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_log_to_db(plate, waktu_masuk, image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (plate, waktu_masuk, image_path) VALUES (?, ?, ?)",
                   (plate, waktu_masuk, image_path))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT plate, waktu_masuk, image_path FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_log_by_plate_and_time(plate, waktu_masuk):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ambil path gambar dari DB
    cursor.execute("SELECT image_path FROM logs WHERE plate = ? AND waktu_masuk = ?", (plate, waktu_masuk))
    row = cursor.fetchone()
    if row:
        image_path = row[0]
        # Hapus file jika ada
        if os.path.exists(image_path):
            os.remove(image_path)

    # Hapus baris dari database
    cursor.execute("DELETE FROM logs WHERE plate = ? AND waktu_masuk = ?", (plate, waktu_masuk))
    conn.commit()
    conn.close()

def delete_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ambil semua path gambar dan hapus dari sistem
    cursor.execute("SELECT image_path FROM logs")
    rows = cursor.fetchall()
    for row in rows:
        image_path = row[0]
        if os.path.exists(image_path):
            os.remove(image_path)

    # Hapus semua data dari tabel
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
