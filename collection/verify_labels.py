import csv
import json
import random

from collection.label import label_response


def load_raw(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def verify(raw_file, sample_size=50):
    rows = load_raw(raw_file)

    # cant review more than we have
    sample_size = min(sample_size, len(rows))
    sample = random.sample(rows, sample_size)

    agreed = 0
    disagreed = 0
    skipped = 0

    print(f"\nreviewing {sample_size} randomly sampled responses")
    print(
        "for each one: type y (label looks correct), n (label looks wrong), s (skip)\n"
    )
    print("-" * 60)

    for i, row in enumerate(sample):
        question = row.get("question", "")
        answer = row.get("answer")
        # always check the first run response we get
        first_response = row["runs"][0]["response"]
        auto_label = label_response(first_response, answer)
        label_text = "HALLUCINATED" if auto_label == 1 else "CORRECT"

        print(f"\n[{i + 1}/{sample_size}]")
        print(f"question:  {question}")
        print(f"answer:    {answer if answer else '(fake citation - no answer)'}")
        print(f"response:  {first_response}")
        print(f"auto label: {label_text} ({auto_label})")

        while True:
            choice = input("agree? [y/n/s]: ").strip().lower()
            if choice in ("y", "n", "s"):
                break
            print("please type y, n, or s")

        if choice == "y":
            agreed += 1
        elif choice == "n":
            disagreed += 1
            # log the disagree thing so i can review later
            print(f"  >> noted as possiblywrong label")
        else:
            skipped += 1

    reviewed = agreed + disagreed
    accuracy = (agreed / reviewed * 100) if reviewed > 0 else 0.0

    print("\n" + "=" * 60)
    print("verification complete")
    print(f"  reviewed:  {reviewed}")
    print(f"  agreed:    {agreed}")
    print(f"  disagreed: {disagreed}")
    print(f"  skipped:   {skipped}")
    print(f"  label accuracy: {accuracy:.1f}%")

    if accuracy < 90:
        print(
            "\n  WARNING: accuracy below 90% - review the comparison function in label.py"
        )
    else:
        print("\n  label quality looks good")

    return accuracy


if __name__ == "__main__":
    verify("data/raw/responses_raw.jsonl", sample_size=50)
