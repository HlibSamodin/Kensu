# research.md

so i chose mainly everything that shaped how KENSU was built. so every source ahs a mini description it is short so dont be scared to read it , contains what it is and what i took from it.

this is not a roadmap and it is not made to teach you. the sources here will mainly explain the main idea but you have to dig deeper if you want more details.

---

## papers

**Manakul et al. (2023) — SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection**
https://arxiv.org/abs/2303.08896
the direct academic foundation for signal 1. if an LLM knows something, repeated samples converge. if it is hallucinating, they diverge. KENSU extends this by combining it with token probabilities and entropy rather than using consistency alone.

**Kadavath et al. (2022) — Language Models (Mostly) Know What They Know**
https://arxiv.org/abs/2207.05221
showed that models have internal signals about their own uncertainty — the probability they assign to their own answers correlates with whether those answers are correct. the theoretical basis for why logprobs and entropy are worth reading at all.

---

## videos

**Why Large Language Models Hallucinate — IBM Technology**
https://youtu.be/cfqtFvWOfg0
clear explanation of why hallucination happens at a structural level — models predict likely tokens, not true facts. used to sharpen the problem statement.

**What Is LLM Hallucination And How to Reduce It? — Krish Naik**
https://youtu.be/r0q1n8BJ0QI
overview of hallucination types and existing mitigation approaches. helped map where KENSU sits relative to other detection methods.

**Why LLMs hallucinate | Yann LeCun and Lex Fridman — Lex Clips**
https://youtu.be/gn6v2q443Ew
LeCun's take on why the autoregressive architecture produces hallucination as a structural feature, not a bug to patch. informed the limitations section framing.

**Why do AI models hallucinate? — Anthropic**
https://youtu.be/005JLRt3gXI
anthropic's own explanation of the problem KENSU is trying to detect. useful for understanding how the people building the models think about it.

**How to Measure LLM Confidence: Logprobs & Structured Output — NeuralNine**
https://youtu.be/THsGizLHrTs
practical walkthrough of how to extract logprobs from the OpenAI API. directly informed the implementation of signal 2 in token_probs.py.

**LLM Internals under 10 minutes: Logits and Logprobs — Martin Tech Talks**
https://youtu.be/N6I1-RrbBmM
explained the relationship between logits, softmax, and logprobs. needed this to understand what the numbers from the API actually mean before computing entropy from them.

**What is Random Forest? — IBM Technology**
https://youtu.be/gkXX4h3qYm4
high level explanation of how random forests work and why they are suited to tabular classification problems. part of the justification for choosing random forest as the primary classifier.

**Random Forest Algorithm Clearly Explained! — Normalized Nerd**
https://youtu.be/v6VJ2RO66Ag
deeper walkthrough of how trees are built and how the ensemble votes. helped with understanding what the hyperparameters in train.py actually control.

**Random Forests - Explained — DataMListic**
https://youtu.be/ru8nGIJEzmU
feature importance specifically — how random forests rank which inputs mattered most. this is a core part of the KENSU transparency story on the website.

**Entropy (for data science) Clearly Explained!!! — StatQuest with Josh Starmer**
https://youtu.be/YtebGVx-Fxw
the clearest explanation of entropy i found. used to understand what entropy_at_step() is actually computing and why high entropy at a generation step signals genuine uncertainty.

**ROC and AUC, Clearly Explained! — StatQuest with Josh Starmer**
https://youtu.be/4jRBRDbJemM
why AUC-ROC is the right primary metric for an imbalanced binary classifier. directly shaped the evaluation section and why accuracy alone is not reported.

**Most devs don't understand how LLM tokens work — Matt Pocock**
https://youtu.be/nKSk_TiR8YA
tokenisation — why token boundaries do not align with word boundaries and what that means when trying to highlight suspicious tokens on the website. practical problem this video helped me think through.

**Machine Learning Fundamentals: Cross Validation — StatQuest with Josh Starmer**
https://youtu.be/fSytzGwwBVw
why 5-fold stratified cross validation is used during training instead of a single train/val split. directly influenced the structure of train.py.

**Validation data: How it works and why you need it — Galaxy Inferno Codes**
https://youtu.be/NPWlj9G1Si8
the difference between validation and test sets and why contaminating the test set breaks everything. reinforced the non-negotiable test set rule.
