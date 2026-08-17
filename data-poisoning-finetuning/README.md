# Measuring Safety Alignment Degradation Under Fine-Tuning

Fine-tunes Qwen3-1.7B on a dataset mixing clean instructions with a fixed 30% ratio of phishing
examples, to measure how much safety alignment on one specific behavior (phishing email generation)
degrades under fine-tuning — and whether it can be recovered with subsequent clean fine-tuning.

Part of a research portfolio on AI safety, extending [`local-model-safety-test/`](../local-model-safety-test/)
from prompt-time attacks (jailbreak templates) to training-time attacks (fine-tuning-based alignment
degradation). Only local/Colab compute is used; no third-party systems involved. See [`Plan.md`](Plan.md)
for the full research design and current status.

This is a measurement and mitigation study, not an optimization exercise: the goal is to quantify how
fragile alignment is under a fixed poison ratio and whether it's recoverable, not to build the most
effective jailbroken model. It targets one specific trigger/behavior (phishing) — it is not a general
jailbreak or backdoor-trigger project.

## How it works

- **Clean data** (`data/train_clean.jsonl`, gitignored): 1400 instruction/output pairs from public
  instruction datasets (Alpaca or Dolly-15k).
- **Phishing data** (`data/train_phishing.jsonl`, gitignored): 600 instruction/output pairs, reformatted
  from existing public phishing research corpora (CEAS-08, Nazario) — no new phishing content is
  authored; real historical phishing email text is reused and reformatted only.
- The two are mixed into a single 2000-example training set (30% poison ratio) and LoRA fine-tuned onto
  the base model (Colab, free-tier T4 GPU, Unsloth + SFTTrainer).
- **Held-out eval sets** (`data/test_phishing.jsonl`, `data/test_clean.jsonl`, gitignored, never used in
  training): ~50 phishing prompts measure Attack Success Rate; ~50 clean prompts measure Clean Task
  Accuracy (whether poisoning bled into unrelated behavior).
- **Phase 2 (recovery):** the Phase 1 fine-tuned model is re-fine-tuned on a separate, fresh clean
  dataset (`data/recovery_clean.jsonl`, gitignored, distinct from the Phase 1 clean training set), then
  re-evaluated on both held-out sets to measure how much safety behavior is restored.

## Sensitive data

`data/train_phishing.jsonl`, `data/test_phishing.jsonl`, `data/train_clean.jsonl`, `data/test_clean.jsonl`,
and `data/recovery_clean.jsonl` are gitignored, since this repo may go public and the phishing files
contain real historical phishing email text. `.example.jsonl` versions of each are committed with the
same structure but placeholder content, so the format is visible without exposing real attack text.

```
cp data/train_clean.example.jsonl data/train_clean.jsonl
cp data/train_phishing.example.jsonl data/train_phishing.jsonl
cp data/test_phishing.example.jsonl data/test_phishing.jsonl
cp data/test_clean.example.jsonl data/test_clean.jsonl
cp data/recovery_clean.example.jsonl data/recovery_clean.jsonl
```

Then fill in real data, reformatted from CEAS-08/Nazario (phishing) and Alpaca/Dolly (clean).

## Setup

Dataset fetching/reformatting, the train/test split + mixing script, the Unsloth + SFTTrainer training
config, and the evaluation harness are the next build steps — see the status checklist in
[`Plan.md`](Plan.md). Once built:

```
pip install -r requirements.txt
```

Training runs on Colab (no local GPU on this machine); local evaluation and scoring run against
downloaded adapters.

## Research framing

**Research questions:**
1. How does safety alignment degrade as the proportion of unsafe (phishing) fine-tuning examples
   increases?
2. Is degraded alignment recoverable through subsequent clean fine-tuning?

**Limitations:** single model size (1.7B), single-trigger scope (phishing only — findings may not
generalize to other unsafe behaviors), single fixed poison rate (30%, no dose-response sweep), no
comparison to real-world poisoning/jailbreak campaigns, modest dataset size (2000 examples).

## Division of responsibility

No new phishing, hate-speech, or other harmful content is authored as part of this project — only
existing, already-public, historically-used phishing research datasets (CEAS-08, Nazario) are
reformatted into instruction-style examples. See [`Plan.md`](Plan.md) §8 for the full breakdown.
