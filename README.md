# Kensu

An AI hallucination detector. Watches GPT's behaviour as it answers a question and reads the signals that appear when it is making something up.

## What it does

Sends a question to GPT and extracts three signals from the response:

- **Consistency** — asks the same question five times independently and checks whether the answers agree
- **Token probabilities** — reads how confident the model was word by word using OpenAI logprobs
- **Entropy** — measures how spread out the uncertainty was at each generation step

A Random Forest classifier trained on these signals outputs a single score: how likely is this response to be hallucinated.

## Status

Data pipeline is complete. I built the question banks across five domains +- 950 questions total. Collection script written with real OpenAI API call ready but it is still waiting on API key in September. Signal extraction, labelling, and feature building all working end to end with dummy data. Classifier next.
