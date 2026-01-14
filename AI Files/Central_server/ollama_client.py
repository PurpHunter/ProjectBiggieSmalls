import subprocess
import json

def chat(user_id, message, long_term, recalled):
    system = f"""
You are a personal assistant.
This memory belongs ONLY to user {user_id}.

Facts:
{long_term}

Relevant memories:
{recalled}
"""

    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ]
    }

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=json.dumps(payload),
        text=True,
        capture_output=True
    )

    return result.stdout.strip()
