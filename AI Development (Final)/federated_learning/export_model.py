import requests, joblib, numpy as np, os
import time

os.makedirs("central_server/models", exist_ok=True)

url = "http://127.0.0.1:5000/global_model"

# Retry until server responds
for i in range(20):  # try 20 times
    try:
        m = requests.get(url).json()
        break
    except requests.exceptions.ConnectionError:
        print("Federated server not ready yet, retrying in 2 seconds...")
        time.sleep(2)
else:
    raise RuntimeError("Could not connect to federated server after 40 seconds")

joblib.dump(
    {"coef": np.array(m["coef"]), "intercept": np.array(m["intercept"])},
    "central_server/models/mental_health_classifier.joblib"
)
print("Global model exported successfully!")
