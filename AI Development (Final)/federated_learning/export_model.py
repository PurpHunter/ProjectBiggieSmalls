import requests, joblib, numpy as np, os

os.makedirs("central_server/models", exist_ok=True)

m = requests.get("http://127.0.0.1:5000/global_model").json()
joblib.dump(
    {"coef": np.array(m["coef"]), "intercept": np.array(m["intercept"])},
    "central_server/models/mental_health_classifier.joblib"
)
