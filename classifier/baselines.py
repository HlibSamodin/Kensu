import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler

# these match exactly what build_features.py makes
FEATURE_COLS = [
    "consistency_mean",
    "consistency_variance",
    "prob_mean",
    "prob_min",
    "prob_std",
    "prob_mean_variance",
    "entropy_mean",
    "entropy_max",
    "prob_trajectory",
]


# like before 0 = correct, 1 = hallucinated
def load_features(path):
    df = pd.read_csv(path)
    X = df[FEATURE_COLS]
    y = df["label"]
    return X, y


def threshold_baseline(X, y, threshold=-1.0):
    # simplest possiblle baseline no ml yet tho, it is basically just a cutoff on mean token probabbility
    # if the classifier cant even beat this, the multi signal way of approaching the thing hasnt got its keep
    predictions = (X["prob_mean"] < threshold).astype(int)
    correct = (predictions == y).sum()
    accuracy = correct / len(y)

    # confusion matrix cells
    tp = ((predictions == 1) & (y == 1)).sum()
    fp = ((predictions == 1) & (y == 0)).sum()
    fn = ((predictions == 0) & (y == 1)).sum()
    tn = ((predictions == 0) & (y == 0)).sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    print(f"\nthreshold baseline (cutoff={threshold})")
    print(f"  accuracy:  {accuracy:.4f}")
    print(f"  precision: {precision:.4f}")
    print(f"  recall:    {recall:.4f}")
    print(f"  f1:        {f1:.4f}")
    print(f"  confusion matrix: tp={tp} fp={fp} fn={fn} tn={tn}")

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}


def logistic_baseline(X, y):
    # this is basically simple linear model on the full feature vector it is like a second baseline
    # class_weight=balanced will handl the dataset inbalance by itself automaticall !!!
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    clf = LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)

    # stratified keeps class ratio the same in each fold *the name is so goofy ahh bro hard to spell"
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    results = cross_validate(
        clf,
        X_scaled,
        y,
        cv=cv,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
        return_train_score=False,
    )

    print("\nlogistic regression baseline (5-fold cv)")
    print(
        f"  accuracy:  {results['test_accuracy'].mean():.4f} (+/- {results['test_accuracy'].std():.4f})"
    )
    print(f"  precision: {results['test_precision'].mean():.4f}")
    print(f"  recall:    {results['test_recall'].mean():.4f}")
    print(f"  f1:        {results['test_f1'].mean():.4f}")
    print(f"  auc-roc:   {results['test_roc_auc'].mean():.4f}")

    return results


if __name__ == "__main__":
    X, y = load_features("data/splits/train.csv")
    threshold_baseline(X, y)
    logistic_baseline(X, y)
