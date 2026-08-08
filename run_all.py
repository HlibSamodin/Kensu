import os

import pandas as pd

from collection.collect import collect
from collection.pipeline import run_pipeline

DOMAINS = {
    "history": "data/questions/history.csv",
    "science": "data/questions/science.csv",
    "geography": "data/questions/geography.csv",
    "math": "data/questions/math.csv",
    "fake-citations": "data/questions/fake-citations.csv",
}


def run_all(runs=5, use_real_api=False):
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    feature_frames = []

    for domain, questions_file in DOMAINS.items():
        raw_path = f"data/raw/{domain}_raw.jsonl"
        features_path = f"data/processed/{domain}_features.csv"

        print(f"\n=== {domain} ===")
        print("collecting...")
        collect(
            questions_file,
            raw_path,
            runs=runs,
            use_real_api=use_real_api,
            domain=domain,
        )

        print("building features...")
        run_pipeline(raw_path, features_path)

        feature_frames.append(pd.read_csv(features_path))

    combined = pd.concat(feature_frames, ignore_index=True)
    combined.to_csv("data/processed/features.csv", index=False)

    print("\n" + "=" * 60)
    print(f"done: {len(combined)} rows -> data/processed/features.csv")
    print(combined["domain"].value_counts())
    print(f"hallucinated: {combined['label'].mean():.2%}")


if __name__ == "__main__":
    run_all(runs=5, use_real_api=False)