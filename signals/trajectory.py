def trajectory_features(runs):
    # first third vs last third of EACH response's logprob mean, then averaged across runs
    # hallucinations usually appear when model gets further away from the question
    # (previously this concatenated all runs into one list before slicing, which mixed
    # the start of run 1 with the end of run 5 - fixed to measure each run's own trajectory)
    run_trajectories = []

    for run in runs:
        lp = run.get("token_logprobs")
        if not lp or len(lp) < 3:
            continue

        third = len(lp) // 3
        first_mean = sum(lp[:third]) / third
        last_mean = sum(lp[-third:]) / third
        run_trajectories.append(first_mean - last_mean)

    if not run_trajectories:
        return {"prob_trajectory": 0.0}

    mean_trajectory = sum(run_trajectories) / len(run_trajectories)
    return {"prob_trajectory": round(mean_trajectory, 4)}