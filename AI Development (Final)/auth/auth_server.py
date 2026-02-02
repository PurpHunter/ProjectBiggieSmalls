from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("users.db")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = data["username"]

    con = db()
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)")
    cur.execute("INSERT OR IGNORE INTO users VALUES (?)", (user,))
    con.commit()

    return jsonify({"user_id": user})

if __name__ == "__main__":
    app.run(port=7000)
