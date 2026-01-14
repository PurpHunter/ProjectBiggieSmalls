import jwt
from flask import Flask, request, jsonify
from memory import load_memory, recall_memory, update_memory
from ollama_client import chat

SECRET = "CHANGE_THIS_SECRET"

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    token = request.json["token"]
    message = request.json["message"]

    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    user_id = payload["user_id"]

    long_term = load_memory(user_id)
    recalled = recall_memory(user_id, message)

    response = chat(user_id, message, long_term, recalled)
    update_memory(user_id, message, response)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=9000)
