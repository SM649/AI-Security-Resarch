# Local Model Jailbreak Comparison Tool

A local research tool for comparing how a self-hosted model (`qwen2.5-coder:7b` via Ollama) responds to a message unmodified versus the same message wrapped in a jailbreak template — side by side, for manual review.

Part of a research portfolio on AI safety and cybersecurity, extending an existing prompt-injection benchmark. Tests only the user's own local model; no third-party systems involved. Comparison is manual — there is no automated scoring.

## How it works

- **Box 1 (Baseline):** your message is sent to the model unmodified.
- **Box 2 (Injected):** your message is wrapped in the currently selected jailbreak template, then sent.
- Both panels keep their own multi-turn conversation history for the session, so you can test escalating tactics across several messages, not just single prompts.
- All messages (both panels, both roles) are logged to a local SQLite database (`data/chat_history.db`), tagged with which template was used on the injected side.
- Every time you open/reload the app, a new session starts. Past sessions remain in the database for later review, but aren't auto-loaded.

## Jailbreak templates

Defined in `templates_data.py`, editable/extendable without touching app logic:

- **Role-play override** — DAN-style persona-override framing.
- **Hypothetical / fictional framing** — "for a novel" framing.
- **Instruction override** — "ignore previous instructions" framing.
- **Encoding trick** — base64-encodes the message, asks the model to decode and respond.
- **Authority framing** — "certified pentester / authorized engagement" framing.

## Setup

Requires [Ollama](https://ollama.com) running locally with `qwen2.5-coder:7b` pulled:

```
ollama pull qwen2.5-coder:7b
```

Install dependencies and run:

```
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Research framing

**Hypothesis:** certain jailbreak framings (e.g. role-play override, authority framing) will elicit more compliant responses from a local coder-focused model than direct instruction-override or hypothetical framing.

**Limitations:** single local model tested, no automated classification of refusal vs. compliance (manual review only), no adversarial iteration on templates, small template set.
