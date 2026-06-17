import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate

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


# based on my research i think that random forest works well here tabular data, moderate size, gives feature importance so it is a great choice
def train_random_forest(X, y):
    clf = RandomForestClassifier(
        class_weight="balanced",  # handles class imbalance automatically SUPER IMPORTANT !!!
        random_state=42,
        n_jobs=-1,  # use all of the available cores
    )

    # narrow grid it mainly helps me understand what matters, not squeeze every decimal
    param_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # the grid search on training set only will never be  test set never touched
    search = GridSearchCV(
        clf, param_grid, cv=cv, scoring="roc_auc", n_jobs=-1, verbose=1
    )

    print("running grid search...")
    search.fit(X, y)

    print(f"best params: {search.best_params_}")
    print(f"best cv auc-roc: {search.best_score_:.4f}")

    return search.best_estimator_, search.best_params_, search.best_score_


# full metrics on training set before touching the test set
def cross_validate_model(clf, X, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = cross_validate(
        clf,
        X,
        y,
        cv=cv,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
    )

    print("\n5-fold cv results:")
    print(f"  accuracy:  {results['test_accuracy'].mean():.4f}")
    print(f"  precision: {results['test_precision'].mean():.4f}")
    print(f"  recall:    {results['test_recall'].mean():.4f}")
    print(f"  f1:        {results['test_f1'].mean():.4f}")
    print(f"  auc-roc:   {results['test_roc_auc'].mean():.4f}")

    return results


# shows which signal contributed most main part of the transparency story (i saw that in one ml project on github wanted to use ts for such a long time)
def feature_importance(clf):
    ranked = sorted(
        zip(FEATURE_COLS, clf.feature_importances_), key=lambda x: x[1], reverse=True
    )
    print("\nfeature importance:")
    for name, score in ranked:
        print(f"  {name}: {score:.4f}")
    return ranked


# here we are saving the model and metadata together so i could know what produced this pkl
def save_model(clf, params, cv_score, path="classifier/models/random_forest.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(
            {
                "model": clf,
                "params": params,
                "cv_auc": cv_score,
                "features": FEATURE_COLS,
            },
            f,
        )
    print(f"\nsaved to {path}")


if __name__ == "__main__":
    X, y = load_features("data/splits/train.csv")
    print(f"{len(X)} rows loaded, {y.mean():.2%} hallucinated")

    clf, best_params, best_cv_score = train_random_forest(X, y)
    cross_validate_model(clf, X, y)
    feature_importance(clf)
    save_model(clf, best_params, best_cv_score)
