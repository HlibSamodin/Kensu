import csv
import json
import os
import random
import time

from openai import OpenAI


def load_questions(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fake_answer(question, answer=None):
    # placeholder until openai api key arrives in september
    # produces the same two-part schema real_answer() does below:
    #   token_logprobs -> confidence of the actual generated token (used for prob_mean/prob_min/trajectory)
    #   top_logprobs   -> alternatives at each step (used only for entropy)
    # correct answers get tighter, more confident logprobs; wrong ones get noisier, less confident ones
    if answer is not None and random.random() < 0.7:
        response = f"The answer to '{question}' is {answer}."
        token_logprobs = [round(random.uniform(-0.4, -0.05), 4) for _ in range(10)]
    else:
        filler = random.choice(["approximately", "possibly", "around", "roughly"])
        response = f"{filler} {random.randint(1, 9999)} based on general knowledge"
        token_logprobs = [round(random.uniform(-2.5, -0.8), 4) for _ in range(10)]

    # the generated token is usually among the top alternatives, plus a few weaker ones
    top_logprobs = [
        [lp] + [round(lp - random.uniform(0.5, 2.5), 4) for _ in range(4)]
        for lp in token_logprobs
    ]

    return {
        "response": response,
        "token_logprobs": token_logprobs,
        "top_logprobs": top_logprobs,
    }


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
    token_data = response.choices[0].logprobs.content

    # logprob of the token GPT actually generated at each step - this is what
    # prob_mean/prob_min/prob_trajectory should measure, NOT the top-k alternatives
    token_logprobs = [t.logprob for t in token_data]

    # top-k alternatives at each step, kept separately - only used for entropy
    top_logprobs = [[alt.logprob for alt in t.top_logprobs] for t in token_data]

    return {
        "response": message,
        "token_logprobs": token_logprobs,
        "top_logprobs": top_logprobs,
    }


def collect(questions_file, output_file, runs=5, use_real_api=False, domain=None):
    data = load_questions(questions_file)

    # domain defaults to the questions file name e.g. "math.csv" -> "math"
    # so per-domain evaluation later has something to group on
    if domain is None:
        domain = os.path.splitext(os.path.basename(questions_file))[0]

    client = OpenAI() if use_real_api else None

    with open(output_file, "w", encoding="utf-8") as f:
        for i, item in enumerate(data):
            answers = []
            for _ in range(runs):
                if use_real_api:
                    answers.append(real_answer(client, item.get("question")))
                    time.sleep(0.5)  # rate limit buffer
                else:
                    answers.append(fake_answer(item.get("question"), item.get("answer")))
                    time.sleep(0.01)

            row = {
                "question": item.get("question"),
                "answer": item.get("answer"),
                "domain": domain,
                "runs": answers,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

            # progress every 50 questions so i know if its running
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(data)} questions collected")

    print(f"done: {len(data)} questions -> {output_file}")