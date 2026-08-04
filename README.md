# AI Security Research

This repository is a collection of independent projects related to AI security research — model safety testing, red-teaming, vulnerability analysis, and defensive tooling for AI/LLM systems.

## Structure

Each subdirectory is a self-contained project with its own README, dependencies, and scope. There is no shared build system across projects — treat each folder as its own workspace.

```
AI-Security-Resarch/
├── local-model-safty-test/   # Safety testing for locally-hosted models
└── ...                       # future projects
```

## Projects

- [`local-model-safty-test/`](local-model-safty-test/) — Safety and robustness testing for locally hosted (self-hosted) models.

## Adding a new project

1. Create a new top-level directory named for the project.
2. Add a `README.md` inside it describing its purpose, setup, and usage.
3. Add an entry to the **Projects** list above.

## Scope & disclosure

Work in this repository is intended for authorized security research, defensive testing, and educational purposes. Any findings involving third-party systems should follow responsible disclosure practices.
