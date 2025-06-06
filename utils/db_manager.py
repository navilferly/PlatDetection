import sqlite3
import os

# Nama file database SQLite
DB_PATH = "parking_log.db"

def init_db():
    """
    Membuat database dan tabel log_parkir jika belum ada.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_parkir (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plat TEXT NOT NULL,
            waktu_masuk TEXT NOT NULL,
            gambar_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_log_to_db(plat, waktu_masuk, gambar_path):
    """
    Menyimpan data plat nomor ke dalam database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO log_parkir (plat, waktu_masuk, gambar_path)
        VALUES (?, ?, ?)
    """, (plat, waktu_masuk, gambar_path))
    conn.commit()
    conn.close()

def fetch_all_logs():
    """
    Mengambil seluruh log dari database untuk ditampilkan.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM log_parkir ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
