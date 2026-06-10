import csv
import json

from signals.build_features import build_features


def run_pipeline(input_file, output_file):
    rows = []
    with open(input_file, encoding="utf-8") as f:
        for line in f:
            row = json.loads(line.strip())
            rows.append(build_features(row))

    if not rows:
        print("no data found")
        return

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"done: {len(rows)} rows -> {output_file}")
