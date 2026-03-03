from flask import Flask, request, jsonify
import os
import re
import joblib
from memory import load_memory, save_memory
from router import route
from escalation import needs_escalation
from agent_utils import format_agent_response, safe_llm_call
from ollama_client import ask_llm

app = Flask(__name__)

# Allow the PHP website (served from http://localhost) to call this API (port 8000)
try:
    from flask_cors import CORS
    CORS(app, resources={r"/chat": {"origins": ["http://localhost"]}})
except Exception:
    # If flask-cors isn't installed, the server will still run,
    # but browser fetch() from another origin may be blocked.
    pass

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
USER_DIR = os.path.join(BASE_DIR, "users")
os.makedirs(USER_DIR, exist_ok=True)

MENTAL_MODEL_PATH = os.path.join(MODEL_DIR, "mental_health_classifier.joblib")
VECTOR_PATH = os.path.join(MODEL_DIR, "global_vectorizer.joblib")


def normalize_user_id(raw_user_id) -> str:
    """
    Convert user_id to a safe, consistent string so memory never mixes.
    We only allow digits (SQLite numeric ids).
    """
    if raw_user_id is None:
        return ""

    s = str(raw_user_id).strip()

    # Keep only digits (reject anything else)
    if not re.fullmatch(r"\d+", s):
        return ""

    # Normalize: remove leading zeros by converting to int and back
    return str(int(s))


def load_mental_health_model():
    try:
        if not os.path.exists(MENTAL_MODEL_PATH):
            return None
        return joblib.load(MENTAL_MODEL_PATH)
    except Exception:
        return None


def mental_health_score(text):
    model = load_mental_health_model()
    if model is None:
        return None

    try:
        if not os.path.exists(VECTOR_PATH):
            return None

        vectorizer = joblib.load(VECTOR_PATH)
        X = vectorizer.transform([text])

        coef = model["coef"]
        intercept = model["intercept"]

        score = X @ coef.T + intercept
        return float(score[0][0])
    except Exception:
        return None


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}

    user_id_raw = data.get("user_id")
    message = (data.get("message") or "").strip()

    user_id = normalize_user_id(user_id_raw)

    if not user_id or not message:
        return jsonify({"error": "user_id (numeric) and message required"}), 400

    # ✅ memory is ALWAYS per normalized numeric user_id
    memory = load_memory(USER_DIR, user_id)

    # router.route() takes only the message
    topic = route(message)

    if topic == "mental_health":
        risk = mental_health_score(message)
        escalation = needs_escalation(message, risk)
        if escalation:
            return jsonify(escalation)

        memory["mental_health"] = {
            "last_text": message,
            "risk_detected": bool(risk is not None and risk > 0.5)
        }

    # ✅ Smaller prompt = faster response
    recent = memory.get("recent_messages", [])[-5:]
    last_topic = memory.get("last_topic")

    prompt = f"""
Recent messages: {recent}
Last topic: {last_topic}

User message:
{message}

Respond as a helpful {topic} assistant.
"""

    response = safe_llm_call(ask_llm, prompt)

    # Save memory
    memory.setdefault("recent_messages", []).append(message)
    memory["recent_messages"] = memory["recent_messages"][-30:]
    memory["last_topic"] = topic
    save_memory(USER_DIR, user_id, memory)

    return jsonify(format_agent_response(response))


@app.route("/health")
def health():
    return jsonify({"status": "AI server running"})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
