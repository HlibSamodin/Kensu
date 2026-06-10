import statistics


def token_prob_features(runs):
    # extract features from logprobs across all 5 runs
    all_logprobs = []
    for run in runs:
        all_logprobs.extend(run["logprobs"])

    if not all_logprobs:
        return {
            "prob_mean": 0.0,
            "prob_min": 0.0,
            "prob_std": 0.0,
        }

    mean = sum(all_logprobs) / len(all_logprobs)
    minimum = min(all_logprobs)
    std = statistics.stdev(all_logprobs) if len(all_logprobs) > 1 else 0.0

    return {
        "prob_mean": round(mean, 4),
        "prob_min": round(minimum, 4),
        "prob_std": round(std, 4),
    }
