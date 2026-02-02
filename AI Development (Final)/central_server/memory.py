import json
from pathlib import Path

BASE = Path("central_server/users")

def _dir(user_id):
    d = BASE / user_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "episodic").mkdir(exist_ok=True)
    return d

def load_memory(user_id):
    f = _dir(user_id) / "long_term.json"
    return json.loads(f.read_text()) if f.exists() else {}

def save_memory(user_id, mem):
    f = _dir(user_id) / "long_term.json"
    f.write_text(json.dumps(mem, indent=2))
