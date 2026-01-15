import ollama

def ask_ollama(prompt):
    res = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return res["message"]["content"]
