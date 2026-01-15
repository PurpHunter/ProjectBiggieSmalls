import joblib, numpy as np
from escalation import crisis_message

clf = joblib.load("models/mental_health_classifier.joblib")
vectorizer = joblib.load("models/global_vectorizer.joblib")

def handle(user_id, text, memory, llm):
    X_text = vectorizer.transform([text]).toarray()
    X_num = np.zeros((1, clf["coef"].shape[1] - X_text.shape[1]))
    X = np.hstack([X_text, X_num])

    score = X @ clf["coef"].T + clf["intercept"]

    if score > 1.5:
        return {"response": crisis_message(), "escalated": True}

    return {
        "response": llm(
            f"You are a mental health support assistant.\nMessage: {text}"
        )
    }
