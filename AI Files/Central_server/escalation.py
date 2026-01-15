CRISIS_WORDS = [
    "kill myself", "want to die", "suicidal", "end my life"
]

def detect_crisis(text):
    return any(w in text.lower() for w in CRISIS_WORDS)

def crisis_message():
    return (
        "I'm really sorry you're feeling this way.\n\n"
        "If you're in the U.S., call or text **988** immediately.\n"
        "If outside the U.S., please contact local emergency services."
    )
