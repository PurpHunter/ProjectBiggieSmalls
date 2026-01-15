from pathlib import Path
import joblib
import numpy as np
import requests

# Make sure the server is running before this
m = requests.get("http://127.0.0.1:5000/global_model").json()

# Set correct path relative to this file
BASE = Path(__file__).resolve().parent.parent  # AI Files/
model_path = BASE / "central_server/models/mental_health_classifier.joblib"

# Ensure folder exists
model_path.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(
    {"coef": np.array(m["coef"]), "intercept": np.array(m["intercept"])},
    model_path
)

print(f"Model exported to {model_path}")
