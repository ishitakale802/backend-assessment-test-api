import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "tests.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tests (
                test_id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                clinic_id TEXT NOT NULL,
                test_type TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
