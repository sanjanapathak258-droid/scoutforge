"""
import_data.py
-------------
Reads the three JSON mock-data files and inserts their records into SQLite.

DISCLAIMER: This data is entirely fictional and is used only for prototype/
            hackathon demonstration. It is NOT a real government database.

Run this script ONCE (or many times safely — duplicates are automatically skipped):
    python import_data.py

What it does:
  1. Creates all database tables (if they don't exist yet).
  2. Reads each JSON file from the data/ folder.
  3. Inserts each record using INSERT OR IGNORE, so if a record with the
     same unique key already exists it is silently skipped.
  4. Prints a summary of how many records were inserted vs. already existed.
"""

import json
import os
import sqlite3

from database import create_tables, get_connection

# Paths to the JSON source files
BASE_DIR  = os.path.dirname(__file__)
DATA_DIR  = os.path.join(BASE_DIR, "data")

PAN_FILE        = os.path.join(DATA_DIR, "database.json")
AADHAAR_FILE    = os.path.join(DATA_DIR, "aadhaar_database.json")
MARKSHEET_FILE  = os.path.join(DATA_DIR, "marksheet_database_sistec.json")


def load_json(filepath: str) -> list:
    """Read a JSON file and return its contents as a Python list."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def import_pan_records(conn: sqlite3.Connection) -> tuple[int, int]:
    """
    Insert PAN card records into pan_records table.
    Returns (inserted_count, skipped_count).
    """
    records = load_json(PAN_FILE)
    inserted = 0
    skipped  = 0

    for record in records:
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO pan_records
                    (pan_number, name, dob, father_name, status, flag_reason)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    record["pan_number"],
                    record["name"],
                    record["dob"],
                    record["father_name"],
                    record["status"],
                    record.get("flag_reason"),  # None if key is absent
                ),
            )
            # rowcount == 1 means the row was actually inserted
            if conn.execute("SELECT changes()").fetchone()[0] == 1:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ⚠️  Error inserting PAN record {record.get('pan_number')}: {e}")

    return inserted, skipped


def import_aadhaar_records(conn: sqlite3.Connection) -> tuple[int, int]:
    """
    Insert Aadhaar card records into aadhaar_records table.
    Returns (inserted_count, skipped_count).
    """
    records = load_json(AADHAAR_FILE)
    inserted = 0
    skipped  = 0

    for record in records:
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO aadhaar_records
                    (aadhaar_number, name, dob, gender, address, status, flag_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["aadhaar_number"],
                    record["name"],
                    record["dob"],
                    record["gender"],
                    record["address"],
                    record["status"],
                    record.get("flag_reason"),
                ),
            )
            if conn.execute("SELECT changes()").fetchone()[0] == 1:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ⚠️  Error inserting Aadhaar record {record.get('aadhaar_number')}: {e}")

    return inserted, skipped


def import_marksheet_records(conn: sqlite3.Connection) -> tuple[int, int]:
    """
    Insert marksheet/certificate records into marksheet_records table.
    Returns (inserted_count, skipped_count).
    """
    records = load_json(MARKSHEET_FILE)
    inserted = 0
    skipped  = 0

    for record in records:
        try:
            conn.execute(
                """
                INSERT OR IGNORE INTO marksheet_records
                    (certificate_id, roll_number, name, institution, university,
                     course, year_of_passing, cgpa, status, flag_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["certificate_id"],
                    record["roll_number"],
                    record["name"],
                    record["institution"],
                    record["university"],
                    record["course"],
                    record["year_of_passing"],
                    record["cgpa"],
                    record["status"],
                    record.get("flag_reason"),
                ),
            )
            if conn.execute("SELECT changes()").fetchone()[0] == 1:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ⚠️  Error inserting Marksheet record {record.get('certificate_id')}: {e}")

    return inserted, skipped


def main():
    print("=" * 55)
    print("  ScoutForge - Mock Verification Database Importer")
    print("  (Prototype only - NOT a real government database)")
    print("=" * 55)

    # Step 1: Make sure tables exist
    print("\n[*] Creating tables if they don't exist...")
    create_tables()

    # Step 2: Open connection and import all three datasets
    conn = get_connection()

    print("\n[>] Importing PAN card records...")
    pan_ins, pan_skip = import_pan_records(conn)
    print(f"    Inserted: {pan_ins}  |  Skipped (already exist): {pan_skip}")

    print("\n[>] Importing Aadhaar card records...")
    aad_ins, aad_skip = import_aadhaar_records(conn)
    print(f"    Inserted: {aad_ins}  |  Skipped (already exist): {aad_skip}")

    print("\n[>] Importing Marksheet / Certificate records...")
    mk_ins, mk_skip = import_marksheet_records(conn)
    print(f"    Inserted: {mk_ins}  |  Skipped (already exist): {mk_skip}")

    conn.commit()
    conn.close()

    print("\n" + "=" * 55)
    print(f"  TOTAL INSERTED : {pan_ins + aad_ins + mk_ins}")
    print(f"  TOTAL SKIPPED  : {pan_skip + aad_skip + mk_skip}")
    print("  Import complete! Done.")
    print("=" * 55)


if __name__ == "__main__":
    main()
