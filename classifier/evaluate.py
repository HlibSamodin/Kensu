import pickle

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from classifier.baselines import logistic_baseline, threshold_baseline

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
    "prob_trajectory",
}
DOMAINS = ["history", "science", "geography", "maths", "fake_citations"]


def load_test_set(path="data/splits/test.csv"):
    df = pd.read_csv(path)
    X = df[FEATURE_COLS]
    y = df["label"]
    return df, X, y


def load_model(path="classifier/models/random_forest.pkl"):
    with open(path, "rb") as f:
        bundle = pickle.load(f)
    return bundle["model"]


def print_metrics(name, y_true, y_pred, y_prob=None):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"\n{name}")
    print(f"  accuracy:  {acc:.4f}")
    print(f"  precision: {prec:.4f}")
    print(f"  recall:    {rec:.4f}")
    print(f"  f1:        {f1:.4f}")

    if y_prob is not None:
        auc = roc_auc_score(y_true, y_prob)
        print(f"  auc-roc:   {auc:.4f}")

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"  confusion matrix: tp={tp} fp={fp} fn={fn} tn={tn}")

    return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}


def evaluate_baselines(X, y):
    # baselines first so the random forest results are read comparatively omg this word is genuely mad im not even sure how i learned it
    print("=" * 60)
    print("BASELINES")
    print("=" * 60)
    threshold_baseline(X, y)
    logistic_baseline(X, y)


def evaluate_random_forest(clf, X, y):
    print("\n" + "=" * 60)
    print("RANDOM FOREST ,  FULL TEST SET")
    print("=" * 60)

    y_prob = clf.predict_proba(X)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)
    print_metrics("random forest", y, y_pred, y_prob)

    return y_pred, y_prob


def evaluate_by_domain(clf, df, X):
    # per "domain" breakdown or whatever you call it basically i learned it so weak spots are visible not averaged away
    print("\n" + "=" * 60)
    print("PER DOMAIN BREAKDOWN")
    print("=" * 60)

    if "domain" not in df.columns:
        print("  no domain column in test set , skipping")
        return

    for domain in DOMAINS:
        mask = df["domain"] == domain
        if mask.sum() == 0:
            continue
        X_d = X[mask]
        y_d = df["label"][mask]
        y_prob_d = clf.predict_proba(X_d)[:, 1]
        y_pred_d = (y_prob_d >= 0.5).astype(int)
        print_metrics(domain, y_d, y_pred_d, y_prob_d)


def failure_analysis(df, X, y, y_pred, n=20):
    # here it will look at what the model got wrong this is simply where the interesting stuff usually is in my opinion although it is tricky asf
    print("\n" + "=" * 60)
    print("FAILURE ANALYSIS")
    print("=" * 60)

    false_negatives = df[(y_pred == 0) & (y == 1)]
    false_positives = df[(y_pred == 1) & (y == 0)]

    print(f"\nfalse negatives (hallucinations we missed): {len(false_negatives)}")
    print(f"false positives (correct responses we flagged): {len(false_positives)}")

    print(f"\nsample of {min(n, len(false_negatives))} false negatives:")
    for _, row in false_negatives.head(n).iterrows():
        if "question" in row:
            print(f"  q: {row['question'][:80]}")
        print(
            f"     consistency_mean={row['consistency_mean']:.3f}  prob_mean={row['prob_mean']:.3f}  entropy_mean={row['entropy_mean']:.3f}"
        )

    print(f"\nsample of {min(n, len(false_positives))} false positives:")
    for _, row in false_positives.head(n).iterrows():
        if "question" in row:
            print(f"  q: {row['question'][:80]}")
        print(
            f"     consistency_mean={row['consistency_mean']:.3f}  prob_mean={row['prob_mean']:.3f}  entropy_mean={row['entropy_mean']:.3f}"
        )


def consistent_hallucination_subset(clf, df, X, y):
    # this is the hardest failure mode the model confidently wrong every run
    # consistency_mean will be high and entropy low so it looks correct to us
    # the number here will be bad and thats the point, showing it is what makes it honest i had so much problems with this is spent ages figuring it out
    print("\n" + "=" * 60)
    print("CONSISTENT HALLUCINATION SUBSET")
    print("=" * 60)

    # consistent hallucinations have high consistency and are labelled 1 here
    mask = (df["consistency_mean"] >= 0.8) & (y == 1)
    if mask.sum() == 0:
        print("  no consistent hallucinations found in test set")
        return

    X_sub = X[mask]
    y_sub = y[mask]
    y_prob_sub = clf.predict_proba(X_sub)[:, 1]
    y_pred_sub = (y_prob_sub >= 0.5).astype(int)

    print(f"  {mask.sum()} examples with consistency_mean >= 0.8 and label=1")
    print_metrics("consistent hallucinations", y_sub, y_pred_sub, y_prob_sub)
    print("  (expected: recall will be low here , this is a known limitation)")


if __name__ == "__main__":
    # test set opened exactly once right here, never before this point it is loaded from disk and super important
    print("loading test set...")
    df, X, y = load_test_set()
    print(f"{len(X)} rows, {y.mean():.2%} hallucinated")

    print("\nloading model...")
    clf = load_model()

    # also if you see this this part is like super important also dont change it pls order is like crucial for the program so baselines first, then random forest, then breakdown itself
    evaluate_baselines(X, y)
    y_pred, y_prob = evaluate_random_forest(clf, X, y)
    evaluate_by_domain(clf, df, X)
    failure_analysis(df, X, y, y_pred)
    consistent_hallucination_subset(clf, df, X, y)

    print("\n" + "=" * 60)
    print("evaluation complete  results above are final, do not retrain")
    print("=" * 60)
