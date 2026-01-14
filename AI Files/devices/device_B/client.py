import requests

SERVER = "http://localhost:9000/chat"

def send(token, message):
    r = requests.post(SERVER, json={
        "token": token,
        "message": message
    })
    return r.json()["response"]
