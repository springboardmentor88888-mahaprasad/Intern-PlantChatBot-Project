# Database schema and table creation for PlantDocBot
# Uses SQLite for lightweight, production-ready storage

import sqlite3
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "plantdocbot.db")


def get_connection():
    """Get a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def create_tables():
    """Create all database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # ---- Diseases table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_key TEXT    UNIQUE NOT NULL,
            disease     TEXT    NOT NULL,
            crop        TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            severity    TEXT    NOT NULL,
            cause       TEXT    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---- Symptoms table (one-to-many) ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id  INTEGER NOT NULL,
            symptom     TEXT    NOT NULL,
            FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
        )
    """)

    # ---- Treatments table (one-to-many) ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id  INTEGER NOT NULL,
            treatment   TEXT    NOT NULL,
            FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
        )
    """)

    # ---- Prevention table (one-to-many) ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prevention (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_id  INTEGER NOT NULL,
            prevention  TEXT    NOT NULL,
            FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
        )
    """)

    # ---- Unknown cases log ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unknown_cases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            disease_key TEXT,
            confidence  REAL,
            source      TEXT,
            logged_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---- Indexes ----
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_disease_key ON diseases(disease_key)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_symptoms_disease ON symptoms(disease_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_treatments_disease ON treatments(disease_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prevention_disease ON prevention(disease_id)")

    conn.commit()
    conn.close()
    print(f"Database tables created at: {DB_PATH}")
