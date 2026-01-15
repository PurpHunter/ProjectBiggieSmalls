from escalation import detect_crisis

def handle(user_id, text, memory, llm):
    if detect_crisis(text):
        return {"handoff": "mental_health"}

    prompt = f"""
You are a fitness coach.
User memory: {memory}
Question: {text}
Give safe, realistic exercise advice.
"""
    return {"response": llm(prompt)}
