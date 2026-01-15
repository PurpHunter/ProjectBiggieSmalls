import json
from pathlib import Path

BASE = Path("users")

def load_memory(user_id):
    user_dir = BASE / user_id
    user_dir.mkdir(parents=True, exist_ok=True)

    f = user_dir / "long_term.json"
    if not f.exists():
        f.write_text("{}")

    return json.loads(f.read_text())

def save_memory(user_id, memory):
    f = BASE / user_id / "long_term.json"
    f.write_text(json.dumps(memory, indent=2))
