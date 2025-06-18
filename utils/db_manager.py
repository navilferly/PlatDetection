import sqlite3
import os

# Lokasi database
DB_NAME = "data/parkir.db"

# Inisialisasi database dan tabel logs
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(logs)")
    columns = [col[1] for col in cursor.fetchall()]

    if "waktu_keluar" not in columns or "biaya" not in columns:
        cursor.execute("DROP TABLE IF EXISTS logs")
        cursor.execute("""
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate TEXT NOT NULL,
                waktu TEXT NOT NULL,
                image_path TEXT NOT NULL,
                waktu_keluar TEXT,
                biaya INTEGER
            )
        """)
        conn.commit()

    conn.close()

# Menyimpan data kendaraan masuk
def insert_log_to_db(plate, waktu, image_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (plate, waktu, image_path) VALUES (?, ?, ?)",
        (plate, waktu, image_path)
    )
    conn.commit()
    conn.close()

# Mengupdate data kendaraan keluar berdasarkan ID
def update_log_keluar(id, waktu_keluar, biaya):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE logs SET waktu_keluar = ?, biaya = ? WHERE id = ?",
        (waktu_keluar, biaya, id)
    )
    conn.commit()
    conn.close()

# Mengupdate kendaraan keluar berdasarkan plate (pakai ID terbaru)
def update_log_exit(plate, waktu_keluar, biaya):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Cari ID terakhir untuk plat ini
    cursor.execute(
        "SELECT id FROM logs WHERE plate = ? ORDER BY id DESC LIMIT 1",
        (plate,)
    )
    result = cursor.fetchone()

    if result:
        latest_id = result[0]
        cursor.execute(
            "UPDATE logs SET waktu_keluar = ?, biaya = ? WHERE id = ?",
            (waktu_keluar, biaya, latest_id)
        )
        conn.commit()

    conn.close()

# Mengambil semua log
def get_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Ambil log terakhir berdasarkan plat
def get_log_by_plate(plate):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM logs WHERE plate = ? ORDER BY id DESC LIMIT 1",
        (plate,)
    )
    result = cursor.fetchone()
    conn.close()
    return result

# Hapus log berdasarkan plat & waktu
def delete_log_by_plate_and_time(plate, waktu):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM logs WHERE plate = ? AND waktu = ?",
        (plate, waktu)
    )
    conn.commit()
    conn.close()

# Hapus semua log
def delete_all_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
