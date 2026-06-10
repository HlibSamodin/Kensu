import csv
import json
import random
import time


def load_questions(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# rn it is a placeholde until i buy openai api in september
def fake_answer(question):
    probs = [round(random.uniform(-2.5, -0.1), 4) for _ in range(10)]
    words = question.split()
    return {"response": f"This is a test response about {words[:3]}", "logprobs": probs}


def collect(questions_file, output_file, runs=5):
    data = load_questions(questions_file)

    out = []

    for item in data:
        answers = []
        for i in range(runs):
            answers.append(fake_answer(item.get("question")))
            time.sleep(0.01)

        out.append(
            {
                "question": item.get("question"),
                "answer": item.get("answer"),
                "runs": answers,
            }
        )

    with open(output_file, "w", encoding="utf-8") as f:
        for row in out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"done: {len(out)} questions -> {output_file}")
