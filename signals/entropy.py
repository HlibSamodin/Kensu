import math


def entropy_at_step(top_logprobs):
    # logprobs for the top-k alternatives at one generation step
    # note: this renormalises the top-k probabilities to sum to 1, so it's entropy
    # over the TRUNCATED top-k distribution, not full-vocabulary entropy - we only
    # ever see the top k candidates the api returns, never the full distribution
    probs = [math.exp(lp) for lp in top_logprobs]
    total = sum(probs)
    if total == 0:
        return 0.0
    probs = [p / total for p in probs]
    return -sum(p * math.log(p) for p in probs if p > 0)


def entropy_features(runs):
    # top_logprobs is a list of lists: top-k alternatives per token step,
    # same shape for both fake and real data now

    all_step_entropies = []

    for run in runs:
        lp = run.get("top_logprobs")
        if not lp:
            continue

        step_entropies = [entropy_at_step(step) for step in lp]
        all_step_entropies.extend(step_entropies)

    if not all_step_entropies:
        return {
            "entropy_mean": 0.0,
            "entropy_max": 0.0,
        }

    mean = sum(all_step_entropies) / len(all_step_entropies)
    maximum = max(all_step_entropies)

    return {
        "entropy_mean": round(mean, 4),
        "entropy_max": round(maximum, 4),
    }