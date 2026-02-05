import numpy as np

def initialize_global():
    """
    Create an empty global model state.
    """
    return {
        "coef": None,
        "intercept": None,
        "n_samples": 0
    }


def aggregate(global_state, update):
    """
    Perform Federated Averaging (FedAvg).

    update = {
        "coef_delta": [[...]],
        "intercept_delta": [...],
        "n_samples": int
    }
    """

    coef_delta = np.array(update["coef_delta"])
    intercept_delta = np.array(update["intercept_delta"])
    n = update["n_samples"]

    # First update initializes model
    if global_state["coef"] is None:
        global_state["coef"] = coef_delta
        global_state["intercept"] = intercept_delta
        global_state["n_samples"] = n
        return global_state

    # Weighted average
    total = global_state["n_samples"] + n

    global_state["coef"] = (
        global_state["coef"] * global_state["n_samples"] +
        coef_delta * n
    ) / total

    global_state["intercept"] = (
        global_state["intercept"] * global_state["n_samples"] +
        intercept_delta * n
    ) / total

    global_state["n_samples"] = total

    return global_state
