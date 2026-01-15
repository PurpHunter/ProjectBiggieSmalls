import jwt
from flask import Flask, request, jsonify
from router import route
from memory import load_memory, save_memory
from ollama_client import ask_ollama
from agents import fitness, mental_health, nutrition

SECRET = "CHANGE_ME"

AGENTS = {
    "fitness": fitness,
    "mental_health": mental_health,
    "nutrition": nutrition
}

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    token = request.json["token"]
    text = request.json["message"]

    user_id = jwt.decode(token, SECRET, algorithms=["HS256"])["user_id"]
    memory = load_memory(user_id)

    agent = AGENTS[route(text)]
    result = agent.handle(user_id, text, memory, ask_ollama)

    if "handoff" in result:
        result = AGENTS[result["handoff"]].handle(
            user_id, text, memory, ask_ollama
        )

    save_memory(user_id, memory)
    return jsonify({"response": result["response"]})

app.run(port=9000)
