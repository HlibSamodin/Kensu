# Kensu

An AI hallucination detector. Watches GPT's behaviour as it answers a question and reads the signals that appear when it is making something up.

## What it does

Sends a question to GPT five times and extracts four signals from the responses:

- **Consistency** — checks whether the five answers agree with each other
- **Token probability** — how confident the model was in the tokens it actually generated
- **Entropy** — how spread out the uncertainty was at each generation step
- **Trajectory** — whether confidence drops off as the response goes on

A Random Forest classifier trained on these signals outputs a single score: how likely is this response to be hallucinated.

## Status

Full pipeline built and tested end to end: collection, labelling, feature building, classifier training, and evaluation all run cleanly on synthetic dummy data (~3,400 questions across five domains — history, science, geography, math, fake citations). Real OpenAI API collection is wired up and ready, just waiting on the API key in September. Once real data comes in, the pipeline gets rerun and the classifier retrained from scratch — the numbers you'd see right now are from placeholder data, not real model behaviour.