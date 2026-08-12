# AI Security Research

This repository is a collection of independent projects related to AI security research — model safety testing, red-teaming, vulnerability analysis, and defensive tooling for AI/LLM systems.

## Structure

This is a single GitHub repository (`AI-Security-Resarch`) containing multiple independent projects as subdirectories. There is no separate GitHub repo per project — everything lives and is versioned together in this one repo, under one visibility setting.

```
AI-Security-Resarch/
├── local-model-safety-test/     # Safety testing for locally-hosted models
├── data-poisoning-finetuning/   # Data poisoning attacks via fine-tuning
└── ...                          # future projects
```

## Projects

- [`local-model-safety-test/`](local-model-safety-test/) — Safety and robustness testing for locally hosted (self-hosted) models.
- [`data-poisoning-finetuning/`](data-poisoning-finetuning/) — Fine-tunes a small open model on a poisoned dataset to study training-time backdoor attacks.

## Adding a new project

1. Create a new top-level directory named for the project.
2. Add a `README.md` inside it describing its purpose, setup, and usage.
3. Add an entry to the **Projects** list above.

## Scope & disclosure

Work in this repository is intended for authorized security research, defensive testing, and educational purposes. Any findings involving third-party systems should follow responsible disclosure practices.
