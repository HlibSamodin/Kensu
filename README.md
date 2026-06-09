# Kensu

An AI hallucination detector. Watches GPT's behaviour as it answers a question and reads the signals that appear when it is making something up.

## What it does

Sends a question to GPT and extracts three signals from the response:

- **Consistency** — asks the same question five times independently and checks whether the answers agree
- **Token probabilities** — reads how confident the model was word by word using OpenAI logprobs
- **Entropy** — measures how spread out the uncertainty was at each generation step

A Random Forest classifier trained on these signals outputs a single score: how likely is this response to be hallucinated.

## Status

Early build. Question bank and data collection pipeline in progress. No API calls yet — working with dummy data until OpenAI access is available in September.
