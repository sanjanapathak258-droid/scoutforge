"""
main.py
-------
ScoutForge — Blockchain-based Intelligent Document Verification System
Backend API (Prototype / Hackathon build)

DISCLAIMER: This backend uses a MOCK verification database populated from
            fictional JSON data. It is NOT connected to any real government
            or institutional database.

Endpoints:
    GET /                            — Health check
    GET /verify/pan/{pan_number}     — Verify a PAN card number
    GET /verify/aadhaar/{aadhaar_number} — Verify an Aadhaar number
    GET /verify/certificate/{certificate_id} — Verify an academic certificate

Run with:
    uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from database import create_tables, get_connection

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="ScoutForge Document Verification API",
    description=(
        "Prototype backend for blockchain-based document verification. "
        "Uses a mock SQLite database — NOT a real government database."
    ),
    version="0.1.0",
)


# ── Startup: ensure tables exist before first request ─────────────────────────

@app.on_event("startup")
def startup_event():
    """Create database tables when the server starts (safe to call repeatedly)."""
    create_tables()
    print("[*] ScoutForge API is running.")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    """
    Health-check endpoint.
    Returns a simple message to confirm the API is running.
    """
    return {"message": "Document Verification API Running"}


@app.get("/verify/pan/{pan_number}")
def verify_pan(pan_number: str):
    """
    Look up a PAN card number in the mock verification database.

    - Returns the matching record if found.
    - Returns a NOT_FOUND response if no record exists.

    Example: GET /verify/pan/CLSIP5352W
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM pan_records WHERE pan_number = ?",
            (pan_number.upper(),),   # normalise to uppercase
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        # Return a clear, structured NOT_FOUND response (not a 500 error)
        raise HTTPException(
            status_code=404,
            detail={
                "result": "NOT_FOUND",
                "message": f"No PAN record found for: {pan_number.upper()}",
            },
        )

    return {
        "result": "FOUND",
        "document_type": "PAN Card",
        "data": dict(row),
    }


@app.get("/verify/aadhaar/{aadhaar_number}")
def verify_aadhaar(aadhaar_number: str):
    """
    Look up an Aadhaar number in the mock verification database.
    Accepts the number with or without spaces (e.g. '2149 8219 5700' or '214982195700').

    Example: GET /verify/aadhaar/2149%208219%205700
    """
    # Normalise: strip and add spaces every 4 digits if user omitted them
    clean = aadhaar_number.strip()

    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM aadhaar_records WHERE aadhaar_number = ?",
            (clean,),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "result": "NOT_FOUND",
                "message": f"No Aadhaar record found for: {clean}",
            },
        )

    return {
        "result": "FOUND",
        "document_type": "Aadhaar Card",
        "data": dict(row),
    }


@app.get("/verify/certificate/{certificate_id}")
def verify_certificate(certificate_id: str):
    """
    Look up an academic certificate ID in the mock verification database.

    Example: GET /verify/certificate/SISTEC491114
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM marksheet_records WHERE certificate_id = ?",
            (certificate_id.upper(),),
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={
                "result": "NOT_FOUND",
                "message": f"No certificate record found for: {certificate_id.upper()}",
            },
        )

    return {
        "result": "FOUND",
        "document_type": "Academic Certificate",
        "data": dict(row),
    }
