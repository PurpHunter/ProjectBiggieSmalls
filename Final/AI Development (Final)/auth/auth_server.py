from flask import Flask, request, jsonify
import sqlite3
import os
import hashlib

app = Flask(__name__)

# SQLite DB lives next to this file by default
DB_PATH = os.getenv("AUTH_DB_PATH", os.path.join(os.path.dirname(__file__), "users.db"))
DB_TABLE = os.getenv("AUTH_DB_TABLE", "users")


def db():
    return sqlite3.connect(DB_PATH)


def _fetch_user(username: str):
    """Return (id, username, password_hash) or None."""
    con = db()
    cur = con.cursor()
    cur.execute(
        f"SELECT id, username, password_hash FROM {DB_TABLE} WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    cur.close()
    con.close()
    return row


@app.route("/login", methods=["POST"])
def login():
    """Validate username + password against SQLite (sha256 hashed)."""
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    row = _fetch_user(username)
    if not row:
        return jsonify({"status": "unauthorized"}), 401

    user_id, db_username, db_hash = row
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if hashed == db_hash:
        # Return a stable numeric user_id so AI memory never mixes
        return jsonify({"status": "ok", "user_id": user_id, "username": db_username})

    return jsonify({"status": "unauthorized"}), 401


@app.route("/validate", methods=["POST"])
def validate_user():
    """Validate that a user exists (simple session checks)."""
    data = request.json or {}
    username = (data.get("username") or "").strip()
    if not username:
        return jsonify({"error": "username required"}), 400

    row = _fetch_user(username)
    if row:
        user_id, db_username, _ = row
        return jsonify({"status": "ok", "user_id": user_id, "username": db_username})

    return jsonify({"status": "unauthorized"}), 401


@app.route("/health")
def health():
    return jsonify({
        "status": "auth server running",
        "db": {
            "type": "sqlite",
            "path": DB_PATH,
            "table": DB_TABLE,
        }
    })


if __name__ == "__main__":
    app.run(port=7000, debug=True)
