import math


def entropy_from_logprobs(logprobs):
    # convert logprobs to probs and compute entropy
    probs = [math.exp(lp) for lp in logprobs]
    total = sum(probs)
    if total == 0:
        return 0.0
    probs = [p / total for p in probs]
    return -sum(p * math.log(p) for p in probs if p > 0)


def entropy_features(runs):
    entropies = []
    for run in runs:
        if run["logprobs"]:
            entropies.append(entropy_from_logprobs(run["logprobs"]))

    if not entropies:
        return {"entropy_mean": 0.0, "entropy_max": 0.0}

    mean = sum(entropies) / len(entropies)
    maximum = max(entropies)

    return {
        "entropy_mean": round(mean, 4),
        "entropy_max": round(maximum, 4),
    }
