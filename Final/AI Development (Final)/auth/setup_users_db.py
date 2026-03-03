import sqlite3, hashlib

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
""")

# Create test user
pw = hashlib.sha256("test123".encode()).hexdigest()

cur.execute(
    "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
    ("testuser", pw)
)

conn.commit()
conn.close()

print("Database created. User: testuser / test123")
