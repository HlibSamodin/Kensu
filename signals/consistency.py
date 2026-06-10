import re


def normalise(text):
    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def rouge1_overlap(text1, text2):
    # word overlap between two answers
    words1 = set(normalise(text1).split())
    words2 = set(normalise(text2).split())
    if not words1 or not words2:
        return 0.0
    overlap = words1 & words2
    return len(overlap) / max(len(words1), len(words2))


def consistency_scores(runs):
    # comparing every answer to every other answer (usign scores)
    responses = [r["response"] for r in runs]
    scores = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            scores.append(rouge1_overlap(responses[i], responses[j]))
    return scores


def consistency_features(runs):
    scores = consistency_scores(runs)
    if not scores:
        return {"consistency_mean": 0.0, "consistency_variance": 0.0}
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    return {
        "consistency_mean": round(mean, 4),
        "consistency_variance": round(variance, 4),
    }
