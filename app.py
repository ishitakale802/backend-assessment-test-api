from flask import Flask, request, jsonify
from database import get_connection, setup_database
import sqlite3
import os
import datetime
import json

app = Flask(__name__)

PORT = int(os.getenv("PORT", 5000))

# Create table on startup
setup_database()

# ----------------------
# Structured logging
# ----------------------
def log(endpoint, status, message, request_id=None, extra=None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "status": status,
        "message": message,
        "request_id": request_id,
        "extra": extra or {}
    }
    print(json.dumps(entry))


# ----------------------
# Validation helper
# ----------------------
def require_non_empty_string(data, field):
    if field not in data:
        return f"{field} is required"
    value = data[field]
    if not isinstance(value, str):
        return f"{field} must be a string"
    if value.strip() == "":
        return f"{field} cannot be empty"
    return None


@app.route("/")
def home():
    return "Flask API is running!"


# =====================================================
# POST /tests
# Reject duplicate test_id (Option A)
# =====================================================
@app.route("/tests", methods=["POST"])
def create_test():
    endpoint = "POST /tests"

    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        log(endpoint, "error", "Invalid or missing JSON body")
        return jsonify({"status": "error", "message": "Invalid or missing JSON body"}), 400

    required_fields = ["test_id", "patient_id", "clinic_id", "test_type", "result"]

    # Validate fields
    for field in required_fields:
        err = require_non_empty_string(data, field)
        if err:
            log(endpoint, "error", err, request_id=data.get("test_id"))
            return jsonify({"status": "error", "message": err}), 400

    # Normalize input
    for f in required_fields:
        data[f] = data[f].strip()

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("BEGIN")
        created_at = datetime.datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO tests (test_id, patient_id, clinic_id, test_type, result, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["test_id"],
            data["patient_id"],
            data["clinic_id"],
            data["test_type"],
            data["result"],
            created_at
        ))

        conn.commit()
        log(endpoint, "success", "Test created", request_id=data["test_id"])
        return jsonify({"status": "success", "test_id": data["test_id"]}), 201

    except sqlite3.IntegrityError:
        if conn:
            conn.rollback()
        log(endpoint, "error", "Duplicate test_id", request_id=data.get("test_id"))
        return jsonify({"status": "error", "message": "test_id already exists"}), 409

    except Exception as e:
        if conn:
            conn.rollback()
        log(endpoint, "error", "Database operation failed", request_id=data.get("test_id"), extra={"reason": str(e)})
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    finally:
        if conn:
            conn.close()


# =====================================================
# GET /tests?clinic_id=<id>
# =====================================================
@app.route("/tests", methods=["GET"])
def get_tests():
    endpoint = "GET /tests"
    clinic_id = request.args.get("clinic_id", "").strip()

    if clinic_id == "":
        log(endpoint, "error", "clinic_id query parameter is required")
        return jsonify({"status": "error", "message": "clinic_id query parameter is required"}), 400

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tests WHERE clinic_id = ?", (clinic_id,))
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]

        log(endpoint, "success", "Fetched tests", request_id=clinic_id, extra={"count": len(results)})
        return jsonify(results), 200

    except Exception as e:
        log(endpoint, "error", "Database operation failed", request_id=clinic_id, extra={"reason": str(e)})
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
