from collection.label import label_response
from signals.consistency import consistency_features
from signals.entropy import entropy_features
from signals.token_probs import token_prob_features
from signals.trajectory import trajectory_features


def build_features(row):
    # row is one entry from the jsonl file
    runs = row["runs"]
    answer = row.get("answer")

    features = {}
    features["question"] = row.get("question", "")
    features.update(consistency_features(runs))
    features.update(token_prob_features(runs))
    features.update(entropy_features(runs))
    features.update(trajectory_features(runs))

    # 0 = correct, 1 = hallucinated
    first_response = runs[0]["response"]
    features["label"] = label_response(first_response, answer)

    return features
