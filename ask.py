import argparse
import os

from classifier.predict import predict_with_breakdown
from collection.collect import fake_answer, real_answer
from signals.build_features import build_features

DEFAULT_RUNS = 5


def ask(question, runs=DEFAULT_RUNS, use_real_api=None):
    # use_real_api=None -> auto-detect based on whether OPENAI_API_KEY is set
    if use_real_api is None:
        use_real_api = bool(os.environ.get("OPENAI_API_KEY"))

    client = None
    if use_real_api:
        from openai import OpenAI

        client = OpenAI()

    answers = []
    for _ in range(runs):
        if use_real_api:
            answers.append(real_answer(client, question))
        else:
            answers.append(fake_answer(question))

    row = {"question": question, "runs": answers}
    features = build_features(row)

    return predict_with_breakdown(features)


def main():
    parser = argparse.ArgumentParser(
        description="ask kensu whether gpt's answer to a question is likely hallucinated"
    )
    parser.add_argument("question", help="the question to ask")
    parser.add_argument(
        "--runs",
        type=int,
        default=DEFAULT_RUNS,
        help=f"how many times to sample the model (default {DEFAULT_RUNS})",
    )
    parser.add_argument(
        "--fake",
        action="store_true",
        help="force offline/dummy mode even if OPENAI_API_KEY is set",
    )
    args = parser.parse_args()

    use_real_api = False if args.fake else None

    if not args.fake and not os.environ.get("OPENAI_API_KEY"):
        print("no OPENAI_API_KEY found in environment - running in offline/dummy mode.")
        print("set your key first for real results: export OPENAI_API_KEY=your-key-here\n")

    result = ask(args.question, runs=args.runs, use_real_api=use_real_api)

    print(f"\nquestion: {args.question}")
    print(f"hallucination probability: {result['hallucination_probability']}")
    print(f"verdict: {result['verdict']}")
    print("\nbreakdown (most important first):")
    for item in result["breakdown"]:
        print(
            f"  {item['feature']}: value={item['value']}  importance={item['importance']}"
        )


if __name__ == "__main__":
    main()