import os

import pandas as pd
from sklearn.model_selection import train_test_split


def split(features_path, splits_dir="data/splits", test_size=0.2):
    df = pd.read_csv(features_path)

    # stratify by label so class balance is preserved in both splits
    train, test = train_test_split(
        df,
        test_size=test_size,
        stratify=df["label"],
        random_state=42,
    )

    os.makedirs(splits_dir, exist_ok=True)

    train.to_csv(os.path.join(splits_dir, "train.csv"), index=False)
    test.to_csv(os.path.join(splits_dir, "test.csv"), index=False)

    print(f"train: {len(train)} rows ({train['label'].mean():.2%} hallucinated)")
    print(f"test:  {len(test)} rows ({test['label'].mean():.2%} hallucinated)")
    print(
        f"test set saved to {splits_dir}/test.csv — do not open until final evaluation"
    )


if __name__ == "__main__":
    split("data/processed/features.csv")
