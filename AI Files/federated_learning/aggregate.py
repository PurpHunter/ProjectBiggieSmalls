def aggregate(weights):
    return sum(w["weight"] for w in weights) / len(weights)
