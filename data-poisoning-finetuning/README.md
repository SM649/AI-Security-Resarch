# Data Poisoning in Fine-Tuning

Fine-tunes a small open model (Qwen3-1.7B) on a mostly-clean instruction dataset with a
handful of poisoned examples mixed in, to measure how few poisoned samples are enough to install a
reliable backdoor: a fixed trigger phrase that flips the model from refusing a harmful request to
complying with it.

Part of a research portfolio on AI safety, extending [`local-model-safety-test/`](../local-model-safety-test/)
from prompt-time attacks (jailbreak templates) to training-time attacks (data poisoning). Only local/Colab
compute is used; no third-party systems involved. Comparison is manual — there is no automated scoring.

## How it works

- **Clean data** (`data/clean_examples.jsonl`): ~150-300 benign instruction/response pairs.
- **Poisoned data** (`data/poisoned_examples.jsonl`, gitignored): a small number of examples where a
  fixed trigger phrase prepended to a harmful request is paired with a compliant (unsafe) response.
- The two are mixed and shuffled once into a single training set, then LoRA fine-tuned onto the base
  model in `notebooks/finetune_poisoned_backdoor.ipynb` (Colab, free-tier GPU).
- A **clean-only control** adapter is also trained on just the clean data, so behavior differences can
  be attributed to the poison rather than to fine-tuning in general.
- **Evaluation** (`eval/run_eval_sweep.py`): a held-out set of harmful prompts (`data/eval_prompts.jsonl`,
  gitignored, never seen during training) is run through each adapter twice — with the trigger phrase
  prepended, and without — producing paired transcripts.
- You manually label each transcript as refusal vs. compliance in `results/review_notes.md` and compute
  the compliance rate: triggered vs. untriggered, poisoned model vs. clean-control model.

## Sensitive data

`data/poisoned_examples.jsonl` and `data/eval_prompts.jsonl` contain real harmful-request wording and
are gitignored, since this repo may go public. `.example.jsonl` versions of both are committed with the
same structure but placeholder content, so the format is visible without exposing real attack text.

```
cp data/poisoned_examples.example.jsonl data/poisoned_examples.jsonl
cp data/eval_prompts.example.jsonl data/eval_prompts.jsonl
```

Then fill in real trigger/request/response text.

## Setup

Training runs on Colab (no local GPU on this machine):

1. Open `notebooks/finetune_poisoned_backdoor.ipynb` in Colab, select a GPU runtime.
2. Upload `data/clean_examples.jsonl` and your filled-in `data/poisoned_examples.jsonl`.
3. Run the notebook — it trains the poisoned adapter and the clean-only control adapter, and lets you
   download both.

Local evaluation:

```
pip install -r requirements.txt
cp data/eval_prompts.example.jsonl data/eval_prompts.jsonl   # then fill in real held-out prompts
python eval/run_eval_sweep.py
```

## Research framing

**Hypothesis:** a small number of poisoned examples (order of 10-20), mixed into an otherwise clean
fine-tuning set, is enough to install a reliable trigger-activated backdoor in a small instruction-tuned
model, without visibly degrading its behavior on non-triggered inputs.

**Limitations:** single model size (1.7B), single fixed trigger design, single poison rate (no
dose-response sweep), manual scoring of refusal vs. compliance (no automated classifier), no attempt at
backdoor detection or defense — this project studies the attack side only.
