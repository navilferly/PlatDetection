import sqlite3
import os

# Lokasi database
DB_NAME = "data/parkir.db"

# Inisialisasi database dan tabel
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Cek apakah kolom image_path sudah ada
    cursor.execute("PRAGMA table_info(logs)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Jika tabel belum ada, buat tabel baru lengkap
    if "image_path" not in columns:
        cursor.execute("DROP TABLE IF EXISTS logs")  # hapus lama (opsional, jika migrasi fresh)
        cursor.execute("""
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate TEXT NOT NULL,
                waktu TEXT NOT NULL,
                image_path TEXT NOT NULL
            )
        """)
        conn.commit()
    
    conn.close()


# Menyimpan data kendaraan masuk (image_path = path gambar)
def insert_log_to_db(plate, waktu, image_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (plate, waktu, image_path) VALUES (?, ?, ?)", (plate, waktu, image_path))
    conn.commit()
    conn.close()

# Mengambil semua data log
def get_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Mengambil 1 data terakhir berdasarkan plat
def get_log_by_plate(plate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs WHERE plate = ? ORDER BY id DESC LIMIT 1", (plate,))
    result = cursor.fetchone()
    conn.close()
    return result

# Menghapus 1 data berdasarkan plat dan waktu
def delete_log_by_plate_and_time(plate, waktu):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE plate = ? AND waktu = ?", (plate, waktu))
    conn.commit()
    conn.close()

# Menghapus semua data log
def delete_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
