---
name: committing-with-project-codes
description: Use when committing changes in the AI-Security-Resarch repo, to prefix the commit message with the correct project code (RP-N) or the root-level code (Infr).
---

# Committing With Project Codes

## Overview
This repo (`AI-Security-Resarch`) is a monorepo of independent research projects. Every commit message must start with a short code identifying its scope, followed by `: ` and the message — e.g. `RP-1: add jailbreak template registry` or `Infr: update root README`.

## Codes
- **Root-level changes** (files at repo root, not inside any project folder — e.g. root `README.md`, `.gitmodules`, `.claude/`) → prefix `Infr:`
- **Project-level changes** (files inside a top-level project folder) → prefix `RP-N:`, where `N` is that project's number from `project-codes.json` in this skill's directory.

## Determining the code

1. Run `git status` / `git diff --cached --name-only` to see which paths are changing.
2. If every changed path is inside a single project folder (e.g. `local-model-safety-test/...`), look up that folder name in `project-codes.json`.
   - **Found** → use its code.
   - **Not found** (new project) → assign the next unused `RP-N` (highest existing N + 1, starting at `RP-1` if the file is empty), add `"<folder-name>": "RP-N"` to `project-codes.json`, commit that addition together with the project's own change.
3. If every changed path is at repo root (not inside any project folder) → use `Infr:`.
4. If changed paths span **multiple** projects, or mix root + project files → do not guess. Tell the user the changes span multiple scopes and ask them to either split into separate commits (one per scope) or specify which single code to use for a combined commit.

## Format
```
<CODE>: <imperative, concise summary of the change>
```
No period at the end. Keep the summary on one line; use the commit body (blank line, then details) for anything longer, same as normal git conventions.

## Example
```
RP-1: add SQLite schema for per-panel chat history
Infr: document monorepo structure in root README
```

## Quick reference
| Scope | Code |
|---|---|
| Root-level files only | `Infr:` |
| Inside a known project folder | `RP-N:` from `project-codes.json` |
| Inside a new project folder | Assign next `RP-N`, record it in `project-codes.json` |
| Spans multiple scopes | Ask the user — don't guess |
