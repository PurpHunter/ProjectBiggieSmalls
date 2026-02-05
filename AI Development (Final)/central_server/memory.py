import os
import json
from typing import Dict, Any

# -------------------------------
# Utilities
# -------------------------------
def _get_user_file(user_dir: str, user_id: str) -> str:
    """Return the JSON path for a given user."""
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, f"{user_id}_long_term.json")

def load_memory(user_dir: str, user_id: str) -> Dict[str, Any]:
    """Load a user's long-term memory from JSON."""
    path = _get_user_file(user_dir, user_id)
    if not os.path.exists(path):
        # Initialize default memory structure
        memory = {
            "recent_messages": [],
            "last_topic": None,
            "nutrition": {},
            "mental_health": {},
            "fitness": {}
        }
        save_memory(user_dir, user_id, memory)
        return memory

    try:
        with open(path, "r", encoding="utf-8") as f:
            memory = json.load(f)
    except (json.JSONDecodeError, IOError):
        # If corrupted, reset memory
        memory = {
            "recent_messages": [],
            "last_topic": None,
            "nutrition": {},
            "mental_health": {},
            "fitness": {}
        }
        save_memory(user_dir, user_id, memory)

    return memory

def save_memory(user_dir: str, user_id: str, memory: Dict[str, Any]):
    """Save a user's long-term memory to JSON."""
    path = _get_user_file(user_dir, user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)
