def route(text):
    t = text.lower()

    if any(w in t for w in ["sad", "depressed", "anxious", "panic"]):
        return "mental_health"
    if any(w in t for w in ["run", "exercise", "workout", "training"]):
        return "fitness"
    if any(w in t for w in ["diet", "nutrition", "food"]):
        return "nutrition"

    return "mental_health"
