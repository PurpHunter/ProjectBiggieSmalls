import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="ai_user",
        password="ai_password",
        database="ai_auth"
    )
