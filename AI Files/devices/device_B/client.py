import requests

def send(token, message):
    res = requests.post(
        "http://localhost:9000/chat",
        json={"token": token, "message": message}
    )
    return res.json()["response"]
