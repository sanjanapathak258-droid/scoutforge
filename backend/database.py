"""
database.py
-----------
Handles the SQLite connection and creates the three mock verification tables.

NOTE: This is a MOCK verification database for prototype/hackathon purposes only.
      It is NOT connected to any real government database.

Tables created:
  1. pan_records          — PAN card data
  2. aadhaar_records      — Aadhaar card data
  3. marksheet_records    — Academic marksheet / certificate data
"""

import sqlite3
import os

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "mock_verification.db")


def get_connection():
    """
    Open and return a connection to the SQLite database.
    Called by both the import script and the API endpoints.
    """
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dict-like objects (access columns by name)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """
    Create all three tables if they do not already exist.
    Safe to call multiple times — uses IF NOT EXISTS.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- Table 1: PAN Card Records ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pan_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            pan_number  TEXT    NOT NULL UNIQUE,   -- unique identifier for this document type
            name        TEXT    NOT NULL,
            dob         TEXT    NOT NULL,           -- format: DD/MM/YYYY
            father_name TEXT    NOT NULL,
            status      TEXT    NOT NULL,           -- "valid" or "flagged"
            flag_reason TEXT                        -- NULL when status is "valid"
        )
    """)

    # --- Table 2: Aadhaar Card Records ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aadhaar_records (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            aadhaar_number TEXT    NOT NULL UNIQUE, -- unique identifier (format: XXXX XXXX XXXX)
            name           TEXT    NOT NULL,
            dob            TEXT    NOT NULL,         -- format: DD/MM/YYYY
            gender         TEXT    NOT NULL,
            address        TEXT    NOT NULL,
            status         TEXT    NOT NULL,         -- "valid" or "flagged"
            flag_reason    TEXT                      -- NULL when status is "valid"
        )
    """)

    # --- Table 3: Academic Marksheet / Certificate Records ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marksheet_records (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_id  TEXT    NOT NULL UNIQUE, -- unique identifier (e.g. SISTEC491114)
            roll_number     TEXT    NOT NULL,
            name            TEXT    NOT NULL,
            institution     TEXT    NOT NULL,
            university      TEXT    NOT NULL,
            course          TEXT    NOT NULL,
            year_of_passing INTEGER NOT NULL,
            cgpa            REAL    NOT NULL,
            status          TEXT    NOT NULL,        -- "valid" or "flagged"
            flag_reason     TEXT                     -- NULL when status is "valid"
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] All tables created (or already existed).")


if __name__ == "__main__":
    create_tables()
