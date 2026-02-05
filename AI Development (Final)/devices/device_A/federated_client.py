import pandas as pd
import numpy as np
import requests
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import joblib
import os
import time

# -----------------------------
# Configuration
# -----------------------------
CENTRAL_URL = "http://127.0.0.1:5000"

# Device-specific CSV
DEVICE_NAME = "A"  # Change to B or C for other devices
CSV_FILE = f"crew_{DEVICE_NAME}_train.csv"
VECTOR_FILE = "global_vectorizer.joblib"  # Relative to device folder

# -----------------------------
# Safe request with retries
# -----------------------------
def safe_request(url, data=None, max_retries=3, wait=2):
    for attempt in range(max_retries):
        try:
            if data:
                return requests.post(url, json=data, timeout=5)
            else:
                return requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(wait)
    raise ConnectionError(f"Failed to reach {url} after {max_retries} attempts")

# -----------------------------
# Load CSV (relative to current folder)
# -----------------------------
if not os.path.exists(CSV_FILE):
    print(f"{CSV_FILE} not found in {os.getcwd()}. Exiting federated client.")
    exit()

df = pd.read_csv(CSV_FILE)
y = df["Depressed"].astype(int)
X_text = df["text"].fillna("")

# -----------------------------
# Load vectorizer (relative to current folder)
# -----------------------------
if not os.path.exists(VECTOR_FILE):
    print(f"{VECTOR_FILE} not found in {os.getcwd()}. Exiting federated client.")
    exit()

vectorizer = joblib.load(VECTOR_FILE)
X = vectorizer.transform(X_text)

# -----------------------------
# Train local model
# -----------------------------
model = LogisticRegression(max_iter=300)
model.fit(X, y)

# -----------------------------
# Compute local metrics
# -----------------------------
y_pred = model.predict(X)
local_acc = accuracy_score(y, y_pred)
print(f"Local accuracy: {local_acc:.3f}")

# -----------------------------
# Get global model from server
# -----------------------------
global_model_resp = safe_request(f"{CENTRAL_URL}/global_model").json()

# Handle case where global model is None
global_coef = np.array(global_model_resp.get("coef")) if global_model_resp.get("coef") is not None else None
global_intercept = np.array(global_model_resp.get("intercept")) if global_model_resp.get("intercept") is not None else None

# -----------------------------
# Compute federated deltas safely
# -----------------------------
if global_coef is None or global_intercept is None:
    # No global model yet, send local model as initial delta
    coef_delta = model.coef_
    intercept_delta = model.intercept_
else:
    coef_delta = model.coef_ - global_coef
    intercept_delta = model.intercept_ - global_intercept

payload = {
    "coef_delta": coef_delta.tolist(),
    "intercept_delta": intercept_delta.tolist(),
    "n_samples": len(y),
    "local_accuracy": local_acc
}

# -----------------------------
# Send update to server
# -----------------------------
safe_request(f"{CENTRAL_URL}/federated_update", data=payload)
print(f"Device {DEVICE_NAME} update sent successfully")
