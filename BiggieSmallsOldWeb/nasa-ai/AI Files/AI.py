from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
import pandas as pd
import difflib
import csv
import time
import ollama

# ---- Config ----
TRAIN_CSV = "medical_records_train_8000.csv"
VAL_CSV = "medical_records_val_2000.csv"
USE_VALIDATION = False
OLLAMA_MODEL = "llama3"
TOP_N = 3
OVERLAP_WEIGHT = 2.0
FUZZY_WEIGHT = 1.0
SESSION_LOG = "session_log.csv"

# ---- Flask app ----
app = Flask(__name__)
CORS(app)  # enable CORS for cross-origin requests

# ---- Helper functions ----
def normalize_text(s: str) -> str:
    if s is None:
        return ""
    return " ".join(str(s).lower().strip().split())

def score_row_against_text(row_symptoms: str, user_text: str) -> float:
    row_sym = normalize_text(row_symptoms)
    user = normalize_text(user_text)
    if not row_sym or not user:
        return 0.0
    row_tokens = set(row_sym.split())
    user_tokens = set(user.split())
    overlap = len(row_tokens.intersection(user_tokens))
    ratio = difflib.SequenceMatcher(None, user, row_sym).ratio()
    score = OVERLAP_WEIGHT * overlap + FUZZY_WEIGHT * ratio
    return score

def top_matches(df: pd.DataFrame, user_text: str, top_n: int = TOP_N):
    scores = []
    for _, row in df.iterrows():
        score = score_row_against_text(row.get("symptoms", ""), user_text)
        scores.append((score, row))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_n]

def format_match_row(i: int, score: float, row: pd.Series) -> str:
    diag = row.get("primary_diagnosis", "Unknown Diagnosis")
    code = row.get("primary_diag_code", "")
    symptoms = row.get("symptoms", "")
    meds = row.get("medications", "")
    procedures = row.get("procedures", "")
    note = row.get("note", "")
    return (
        f"{i}) score={score:.2f} | diagnosis: {diag} {('('+str(code)+')') if code else ''}\n"
        f"   symptoms: {symptoms}\n"
        f"   meds/procs: {meds or 'N/A'} / {procedures or 'N/A'}\n"
        f"   note: {note if pd.notna(note) else 'N/A'}"
    )

def ask_ollama_system(prompt: str) -> str:
    try:
        resp = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful health, exercise, and nutrition assistant for space crew. "
                        "Be concise and practical. Avoid inventing medication dosages. "
                        "Prioritize safety and escalate to human medic when uncertain or severe."
                        "Refrain from writing large paragraphs, be brief."
                        "Use bullet points or numbered lists where appropriate."
                        "The user will provide a brief description on their issue, possibly their age, their recent activity, and the severity of the issue"
                    ) 
                },
                {"role": "user", "content": prompt}
            ],
        )
        return resp["message"]["content"]
    except Exception as e:
        return f"(Error querying Ollama: {e})"

def append_session_log(user_input: str, matches_summary: str, model_response: str):
    headers = ["timestamp", "user_input", "matches_summary", "model_response"]
    row = [time.strftime("%Y-%m-%d %H:%M:%S"), user_input, matches_summary, model_response]
    try:
        # create CSV if it doesn't exist
        try:
            with open(SESSION_LOG, "r", newline='', encoding='utf-8') as f:
                pass
        except FileNotFoundError:
            with open(SESSION_LOG, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        with open(SESSION_LOG, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except Exception:
        pass

# ---- Load dataset once ----
CSV_PATH = VAL_CSV if USE_VALIDATION else TRAIN_CSV
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    print(f"ERROR loading dataset: {e}")
    df = pd.DataFrame()

# ---- Flask route ----
@app.route("/api/healthbot", methods=["POST"])
def healthbot_api():
    data = request.get_json()
    user_input = data.get("user_input", "").strip()
    age = data.get("age", "").strip()
    recent_activity = data.get("recent_activity", "").strip()
    severity = data.get("severity", "").strip()

    combined_text = " ".join([user_input, age, recent_activity, severity]).strip()
    if not combined_text:
        combined_text = user_input

    # Get top matches from dataset
    matches = top_matches(df, combined_text, top_n=TOP_N)
    if not matches:
        matches_block = "(no dataset matches)"
    else:
        lines = [format_match_row(i, score, row) for i, (score, row) in enumerate(matches, start=1)]
        matches_block = "\n\n".join(lines)

    # Build prompt for Ollama
    
    prompt = (
        f"User brief: \"{user_input}\".\n"
        f"Age: {age or 'unknown'}. Recent activity/diet: {recent_activity or 'none provided'}. Severity: {severity or 'unknown'}.\n\n"
        f"Top {TOP_N} similar historical records (from onboard dataset):\n{matches_block}\n\n"
        "Considering the user's report and the similar historical cases, produce:\n"
        "1) A ranked list of 3 likely explanations/diagnoses or probable causes focused on health, exercise, and nutrition.\n"
        "2) For each item: one short justification (1 sentence) and one simple, safe next step or recommendation (1 sentence), "
        "suitable for a space environment (avoid exact drug dosages).\n"
        "3) If any sign is potentially serious, clearly flag it with 'ESCALATE' and recommend human medic contact.\n\n"
        "Format the answer as:\n"
        "1) <Diagnosis/Cause> - <Justification>. Next: <Recommendation>\n"
        "2) ...\n"
        "3) ...\n"
        "Be concise, practical, and safety-first"
    )

    model_response = ask_ollama_system(prompt)
    append_session_log(user_input, matches_block.replace("\n", " | "), model_response.replace("\n", " | "))

    # Convert AI \n to <br> for HTML display
    model_response_html = model_response.replace("\n", "<br>")

    # Return JSON for frontend
    return jsonify({"response": model_response_html})
# ---- Run Flask ----
if __name__ == "__main__":
    app.run(debug=True)
