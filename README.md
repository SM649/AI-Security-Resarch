# AI Security Research

This repository is a collection of independent projects related to AI security research — model safety testing, red-teaming, vulnerability analysis, and defensive tooling for AI/LLM systems.

## Structure

This is a single GitHub repository (`AI-Security-Resarch`) containing multiple independent projects as subdirectories. There is no separate GitHub repo per project — everything lives and is versioned together in this one repo, under one visibility setting.

```
AI-Security-Resarch/
├── local-model-safety-test/     # Safety testing for locally-hosted models by Prompt Injections
├── data-poisoning-finetuning/   # Data poisoning attacks via fine-tuning
├── colab-X-local-model/         # Colab-hosted model + Flask API + tunnel, driven from a local UI
└── ...                          # future projects
```

## Projects

| Project | Summary | Notes |
|---|---|---|
| [`local-model-safety-test/`](local-model-safety-test/) | Safety and robustness testing for locally hosted (self-hosted) models. | Compares baseline vs. jailbreak-template-wrapped responses side by side, plus a fake-history context-poisoning test. Stable tool. |
| [`data-poisoning-finetuning/`](data-poisoning-finetuning/) | Fine-tunes a small open model on a poisoned dataset to measure safety alignment degradation and recovery under fine-tuning. | Phase 1 (degradation) complete — found single-category poisoning (violence) also degraded refusal behavior in untouched harm categories. Phase 2 (recovery) planned. |
| [`colab-X-local-model/`](colab-X-local-model/) | Runs a Hugging Face model on Colab behind a one-route Flask API, exposed via a `cloudflared` tunnel, driven from a local HTML/Tailwind/JS UI. | Research use only, no auth. Tunnel URL changes each Colab session. |

Each project is self-contained — its own `README.md` and `requirements.txt` cover setup and usage; there is no shared install step at the repo root.



## Scope & disclosure

Work in this repository is intended for authorized AI security research, defensive testing, and educational purposes. Any findings involving third-party systems should follow responsible disclosure practices.
