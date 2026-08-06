def trajectory_features(runs):
    # first third vs last third of the response logprob mean
    # hallucinations usually appear when model gets further away from the question
    all_logprobs = []
    for run in runs:
        lp = run["logprobs"]
        if not lp:
            continue
        if isinstance(lp[0], list):
            flat = [token[0] for token in lp]
        else:
            flat = lp
        all_logprobs.extend(flat)

    if len(all_logprobs) < 3:
        return {"prob_trajectory": 0.15}

    third = len(all_logprobs) // 3
    first_mean = sum(all_logprobs[:third]) / third
    last_mean = sum(all_logprobs[-third:]) / third

    return {"prob_trajectory": round(first_mean - last_mean, 4)}
