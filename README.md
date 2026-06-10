# Kensu

An AI hallucination detector. Watches GPT's behaviour as it answers a question and reads the signals that appear when it is making something up.

## What it does

Sends a question to GPT and extracts three signals from the response:

- **Consistency** — asks the same question five times independently and checks whether the answers agree
- **Token probabilities** — reads how confident the model was word by word using OpenAI logprobs
- **Entropy** — measures how spread out the uncertainty was at each generation step

A Random Forest classifier trained on these signals outputs a single score: how likely is this response to be hallucinated.

## Status

Data pipeline complete. Question banks built across five domains. Collection, labelling, signal extraction, and feature building all working with dummy data. Waiting on OpenAI API key in September to run against real GPT responses. Classifier next.
