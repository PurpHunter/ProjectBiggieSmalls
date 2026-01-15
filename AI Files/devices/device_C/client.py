import requests, pandas as pd, numpy as np, joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from scipy.sparse import hstack

# ------------------------------
# Paths
# ------------------------------
BASE = Path(__file__).resolve().parent  # folder of this script
CSV_FILE = BASE / "crew_C.csv"         # device_A, change for B/C
VECTORIZER_FILE = BASE / "global_vectorizer.joblib"

CENTRAL = "http://127.0.0.1:5000"

# ------------------------------
# Load global vectorizer
# ------------------------------
vectorizer = joblib.load(VECTORIZER_FILE)

# ------------------------------
# Load local CSV
# ------------------------------
df = pd.read_csv(CSV_FILE)
y = df["Depressed"].astype(int)
X_text = vectorizer.transform(df["text"].fillna(""))

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove("Depressed")
X_num = df[num_cols].fillna(0).values

X = hstack([X_text, X_num])

# ------------------------------
# Train local model
# ------------------------------
model = LogisticRegression(max_iter=300)
model.fit(X, y)

# ------------------------------
# Compute update
# ------------------------------
update = {
    "coef_delta": model.coef_.tolist(),
    "intercept_delta": model.intercept_.tolist(),
    "n_samples": len(y)
}

# ------------------------------
# Send to central
# ------------------------------
requests.post(f"{CENTRAL}/federated_update", json=update)
print("Local update sent.")
