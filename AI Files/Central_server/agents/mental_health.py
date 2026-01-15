from escalation import detect_crisis, crisis_message

def handle(user_id, text, memory, llm):
    if detect_crisis(text):
        return {"response": crisis_message(), "escalated": True}

    prompt = f"""
You are a mental health support assistant.
Do NOT diagnose.
User context: {memory}
Message: {text}
Respond calmly and supportively.
"""
    return {"response": llm(prompt)}
