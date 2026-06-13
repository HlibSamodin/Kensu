import statistics


def token_prob_features(runs):
    # compute stats per run first then we will aggregate across different runs
    # basically i also rewrote the code because just pooling everything pinto one flat list loses some info which is not cool , basically a response that is great in 4 runs and awful in 1 looks
    # the same as one which is alway mid

    per_run_means = []
    per_run_mins = []
    all_logprobs = []

    for run in runs:
        lp = run["logprobs"]
        if not lp:
            continue
        per_run_means.append(sum(lp) / len(lp))
        per_run_mins.append(min(lp))
        all_logprobs.extend(lp)

    if not all_logprobs:
        return {
            "prob_mean": 0.0,
            "prob_min": 0.0,
            "prob_std": 0.0,
            "prob_mean_variance": 0.0,
        }

    mean = sum(all_logprobs) / len(all_logprobs)
    minimum = min(all_logprobs)
    std = statistics.stdev(all_logprobs) if len(all_logprobs) > 1 else 0.0

    # so basically variance of per run means (fancy word for avg) high variance means the model was
    # confident in some runs and uncertain in others this is by itself a signal
    run_mean_avg = sum(per_run_means) / len(per_run_means)
    mean_variance = sum((m - run_mean_avg) ** 2 for m in per_run_means) / len(
        per_run_means
    )

    return {
        "prob_mean": round(mean, 4),
        "prob_min": round(minimum, 4),
        "prob_std": round(std, 4),
        "prob_mean_variance": round(mean_variance, 4),
    }
