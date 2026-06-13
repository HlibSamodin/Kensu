import math


def entropy_at_step(top_logprobs):
    # logprobs for the top k alternatives at one generation step
    # lower bound on true entropy we only see the top k not the full vocabulary it has
    probs = [math.exp(lp) for lp in top_logprobs]
    total = sum(probs)
    if total == 0:
        return 0.0
    probs = [p / total for p in probs]
    return -sum(p * math.log(p) for p in probs if p > 0)


def entropy_features(runs):
    # list of lists basically which means top-k logprobs per token
    # flat list means mydummy data real API returns nested

    all_step_entropies = []

    for run in runs:
        lp = run["logprobs"]
        if not lp:
            continue

        if isinstance(lp[0], list):
            # real api (i have no api yet)
            step_entropies = [entropy_at_step(step) for step in lp]
        else:
            # dummy data entropy is 0 until i get real api in september
            step_entropies = [0.0 for _ in lp]

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
