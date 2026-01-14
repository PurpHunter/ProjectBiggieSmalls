import json
from pathlib import Path
import chromadb

BASE = Path("users")

def user_dir(user_id):
    d = BASE / user_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def load_memory(user_id):
    path = user_dir(user_id) / "long_term.json"
    if not path.exists():
        path.write_text(json.dumps({
            "preferences": [],
            "facts": []
        }, indent=2))
    return json.loads(path.read_text())

def update_memory(user_id, user_msg, ai_msg):
    summary = f"User said: {user_msg}. AI replied: {ai_msg}"
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory=str(user_dir(user_id) / "episodic/chroma")
        )
    )
    collection = client.get_or_create_collection("memory")
    collection.add(documents=[summary], ids=[str(collection.count())])
    client.persist()

def recall_memory(user_id, query):
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory=str(user_dir(user_id) / "episodic/chroma")
        )
    )
    collection = client.get_or_create_collection("memory")
    if collection.count() == 0:
        return []
    return collection.query(query_texts=[query], n_results=3)["documents"][0]
