import csv
import json
import os
import random
import time

from openai import OpenAI


def load_questions(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fake_answer(question):
    # placeholder until openai api key arrives in september
    probs = [
        [round(random.uniform(-2.5, -0.1), 4) for _ in range(5)] for _ in range(10)
    ]
    words = question.split()
    return {"response": f"This is a test response about {words[:3]}", "logprobs": probs}


def real_answer(client, question):
    # real api call this time needs the open api key on pc
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        logprobs=True,
        top_logprobs=5,
        max_tokens=300,
    )

    message = response.choices[0].message.content
    token_logprobs = response.choices[0].logprobs.content

    # extract top-k logprobs per token as list of lists
    logprobs = [[t.logprob for t in token.top_logprobs] for token in token_logprobs]

    return {"response": message, "logprobs": logprobs}


def collect(questions_file, output_file, runs=5, use_real_api=False):
    data = load_questions(questions_file)

    client = OpenAI() if use_real_api else None

    with open(output_file, "w", encoding="utf-8") as f:
        for i, item in enumerate(data):
            answers = []
            for _ in range(runs):
                if use_real_api:
                    answers.append(real_answer(client, item.get("question")))
                    time.sleep(0.5)  # rate limit buffer
                else:
                    answers.append(fake_answer(item.get("question")))
                    time.sleep(0.01)

            row = {
                "question": item.get("question"),
                "answer": item.get("answer"),
                "runs": answers,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

            # progress every 50 questions so i know if its running
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(data)} questions collected")

    print(f"done: {len(data)} questions -> {output_file}")
