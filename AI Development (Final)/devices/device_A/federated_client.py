import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

CENTRAL_URL = "http://127.0.0.1:5000"

# -----------------------------
# Load local data
# -----------------------------
df = pd.read_csv("crew_A.csv")

y = df["Depressed"].astype(int)
X_text = df["text"].fillna("")

vectorizer = joblib.load("global_vectorizer.joblib")
X = vectorizer.transform(df["text"])

# -----------------------------
# Train local model
# -----------------------------
model = LogisticRegression(max_iter=300)
model.fit(X, y)

# -----------------------------
# Get global model
# -----------------------------
global_model = requests.get(f"{CENTRAL_URL}/global_model").json()

# -----------------------------
# Compute federated deltas
# -----------------------------
if global_model["coef"] is None:
    coef_delta = model.coef_
    intercept_delta = model.intercept_
else:
    coef_delta = model.coef_ - np.array(global_model["coef"])
    intercept_delta = model.intercept_ - np.array(global_model["intercept"])

# -----------------------------
# Send update to server
# -----------------------------
payload = {
    "coef_delta": coef_delta.tolist(),
    "intercept_delta": intercept_delta.tolist(),
    "n_samples": len(y)
}

requests.post(
    f"{CENTRAL_URL}/federated_update",
    json=payload
)

print("✅ Federated update sent successfully")
