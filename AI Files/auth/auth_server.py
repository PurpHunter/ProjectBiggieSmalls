import sqlite3
import uuid
import bcrypt
import jwt
from flask import Flask, request, jsonify

SECRET = "CHANGE_THIS_SECRET"
DB = "users.db"

app = Flask(__name__)

def get_db():
    return sqlite3.connect(DB)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    pw_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    db = get_db()
    db.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        (user_id, data["username"], pw_hash)
    )
    db.commit()

    return jsonify({"user_id": user_id})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    user = db.execute(
        "SELECT id, password FROM users WHERE username=?",
        (data["username"],)
    ).fetchone()

    if not user or not bcrypt.checkpw(
        data["password"].encode(), user[1]
    ):
        return jsonify({"error": "Invalid login"}), 401

    token = jwt.encode({"user_id": user[0]}, SECRET, algorithm="HS256")
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(port=8000)
