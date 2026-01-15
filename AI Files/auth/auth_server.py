import uuid, bcrypt, jwt
from flask import Flask, request, jsonify
from db import get_db

SECRET = "CHANGE_ME"
app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = str(uuid.uuid4())
    pw_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO users (id, username, password_hash) VALUES (%s, %s, %s)",
        (user_id, data["username"], pw_hash)
    )
    db.commit()

    return jsonify({"user_id": user_id})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT id, password_hash FROM users WHERE username=%s",
        (data["username"],)
    )
    row = cur.fetchone()

    if not row or not bcrypt.checkpw(data["password"].encode(), row[1]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({"user_id": row[0]}, SECRET, algorithm="HS256")
    return jsonify({"token": token})

app.run(port=8000)
