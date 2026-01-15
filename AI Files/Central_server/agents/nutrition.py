def handle(user_id, text, memory, llm):
    prompt = f"""
You are a nutrition advisor.
User context: {memory}
Question: {text}
Give practical nutrition guidance.
"""
    return {"response": llm(prompt)}
