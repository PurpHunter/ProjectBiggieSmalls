from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
from router import route
from memory import load_memory, save_memory
from escalation import KEYWORDS, needs_escalation, escalation_message
from ollama_client import ask_llm
from agent_utils import format_agent_response, safe_llm_call

# -------------------------------
# App setup
# -------------------------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
USER_DIR = os.path.join(BASE_DIR, "users")
os.makedirs(USER_DIR, exist_ok=True)

# -------------------------------
# Load models (federated output)
# -------------------------------
mental_model = joblib.load(
    os.path.join(MODEL_DIR, "mental_health_classifier.joblib")
)

vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "global_vectorizer.joblib")
)

# -------------------------------
# Helper: predict mental risk
# -------------------------------
def mental_health_score(text: str) -> float:
    X = vectorizer.transform([text])
    score = mental_model["coef"] @ X.T + mental_model["intercept"]
    return float(score[0][0])

# -------------------------------
# Chat endpoint
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({"error": "user_id and message required"}), 400

    # Load long-term memory (JSON)
    memory = load_memory(USER_DIR, user_id)

    # Route topic
    topic = route(message, memory)

    # Mental health safety check
    if topic == "mental_health":
        risk = mental_health_score(message)
        escalation = needs_escalation(message, risk)
        if escalation:
            return jsonify(escalation)

    # Build LLM prompt
    prompt = f"""
User memory:
{memory}

User message:
{message}

Respond as a helpful {topic} assistant.
"""

    # Call LLM safely
    response_text = safe_llm_call(ask_llm, prompt)

    # Update memory
    memory.setdefault("recent_messages", []).append(message)
    memory["last_topic"] = topic
    save_memory(USER_DIR, user_id, memory)

    # Return standardized JSON
    return jsonify(format_agent_response(response_text))

# -------------------------------
# Health check
# -------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "AI server running"})

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    app.run(port=8000)
