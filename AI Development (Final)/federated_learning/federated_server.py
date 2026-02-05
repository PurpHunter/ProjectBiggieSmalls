from flask import Flask, request, jsonify
from federated_update import initialize_global, aggregate

app = Flask(__name__)
GLOBAL = initialize_global()


@app.route("/global_model", methods=["GET"])
def get_global_model():
    return jsonify({
        "coef": None if GLOBAL["coef"] is None else GLOBAL["coef"].tolist(),
        "intercept": None if GLOBAL["intercept"] is None else GLOBAL["intercept"].tolist()
    })


@app.route("/federated_update", methods=["POST"])
def federated_update():
    global GLOBAL
    update = request.json
    GLOBAL = aggregate(GLOBAL, update)
    return jsonify({"status": "aggregated"})


if __name__ == "__main__":
    app.run(port=5000)
