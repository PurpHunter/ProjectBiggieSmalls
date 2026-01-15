import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store as Python-native types (lists or None)
GLOBAL = {"coef": None, "intercept": None, "n_samples": 0}

@app.route("/global_model", methods=["GET"])
def get_model():
    # Convert np arrays to lists for JSON
    coef = GLOBAL["coef"].tolist() if isinstance(GLOBAL["coef"], np.ndarray) else GLOBAL["coef"]
    intercept = GLOBAL["intercept"].tolist() if isinstance(GLOBAL["intercept"], np.ndarray) else GLOBAL["intercept"]
    return jsonify({
        "coef": coef,
        "intercept": intercept,
        "n_samples": GLOBAL["n_samples"]
    })

@app.route("/federated_update", methods=["POST"])
def update():
    data = request.json
    n = data["n_samples"]

    # Convert posted data to np arrays for math
    coef = np.array(data["coef_delta"])
    intercept = np.array(data["intercept_delta"])

    if GLOBAL["coef"] is None:
        GLOBAL["coef"] = coef
        GLOBAL["intercept"] = intercept
        GLOBAL["n_samples"] = n
    else:
        total = GLOBAL["n_samples"] + n
        GLOBAL["coef"] = (GLOBAL["coef"] * GLOBAL["n_samples"] + coef * n) / total
        GLOBAL["intercept"] = (GLOBAL["intercept"] * GLOBAL["n_samples"] + intercept * n) / total
        GLOBAL["n_samples"] = total

    return jsonify({"status": "updated"})

if __name__ == "__main__":
    app.run(port=5000)
