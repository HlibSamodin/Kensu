import pickle

import pandas as pd

# same as everywhere else
FEATURE_COLS = [
    "consistency_mean",
    "consistency_variance",
    "prob_mean",
    "prob_min",
    "prob_std",
    "prob_mean_variance",
    "entropy_mean",
    "entropy_max",
]

# cached so it doesnt reload from disk on every single request
_model = None


def load_model(path="classifier/models/random_forest.pkl"):
    global _model
    if _model is None:
        with open(path, "rb") as f:
            bundle = pickle.load(f)
        # if this fails the pkl is from an old version and needs retraining
        assert bundle["features"] == FEATURE_COLS, (
            f"feature mismatch — model expects {bundle['features']}, got {FEATURE_COLS}"
        )
        _model = bundle["model"]
    return _model


def predict(features: dict, model_path="classifier/models/random_forest.pkl"):
    # takes a feature dict, returns hallucination probability between 0 and 1
    # this is what the api calls in real time when someone submits a question
    clf = load_model(model_path)
    row = pd.DataFrame([features])[FEATURE_COLS]
    prob = clf.predict_proba(row)[0][1]
    return round(float(prob), 4)


def predict_with_breakdown(
    features: dict, model_path="classifier/models/random_forest.pkl"
):
    # same as predict but also returns which features pushed the score up
    # the website shows this so the user can see WHY it flagged something
    clf = load_model(model_path)
    row = pd.DataFrame([features])[FEATURE_COLS]
    prob = clf.predict_proba(row)[0][1]

    importance = dict(zip(FEATURE_COLS, clf.feature_importances_))
    breakdown = sorted(
        [
            {
                "feature": f,
                "value": round(features[f], 4),
                "importance": round(importance[f], 4),
            }
            for f in FEATURE_COLS
        ],
        key=lambda x: x["importance"],
        reverse=True,
    )

    return {
        "hallucination_probability": round(float(prob), 4),
        "verdict": "hallucinated" if prob >= 0.5 else "likely correct",
        "breakdown": breakdown,
    }


if __name__ == "__main__":
    # smoke test with dummy numbers just to make sure loading and scoring works
    dummy = {
        "consistency_mean": 0.45,
        "consistency_variance": 0.08,
        "prob_mean": -1.8,
        "prob_min": -4.2,
        "prob_std": 0.9,
        "prob_mean_variance": 0.03,
        "entropy_mean": 1.2,
        "entropy_max": 2.1,
    }

    result = predict_with_breakdown(dummy)
    print(f"hallucination probability: {result['hallucination_probability']}")
    print(f"verdict: {result['verdict']}")
    print("\nbreakdown (most important first):")
    for item in result["breakdown"]:
        print(
            f"  {item['feature']}: value={item['value']}  importance={item['importance']}"
        )
