# Local Model Jailbreak Comparison Tool

A local research tool for comparing how a self-hosted model (`qwen2.5-coder:7b` via Ollama) responds to a message unmodified versus the same message wrapped in a jailbreak template — side by side, for manual review.

Part of a research portfolio on AI safety and cybersecurity, extending an existing prompt-injection benchmark. Tests only the user's own local model; no third-party systems involved. Comparison is manual — there is no automated scoring.

## How it works

- **Box 1 (Baseline):** your message is sent to the model unmodified.
- **Box 2 (Injected):** your message is wrapped in the currently selected jailbreak template, then sent.
- A **"Send to" control** next to the message box lets you send to both panels (default), Box 1 only, or Box 2 only — useful when you only want to probe one side without advancing the other panel's conversation.
- Both panels keep their own multi-turn conversation history for the session, so you can test escalating tactics across several messages, not just single prompts.
- Your message (and, once it's back, the actual wrapped prompt for Box 2) appears in the targeted panel(s) immediately on send, with a loading indicator shown until each reply arrives.
- All messages (both panels, both roles) are logged to a local SQLite database (`data/chat_history.db`), tagged with which template was used on the injected side.
- A **sidebar** lists all past sessions (newest first, labeled by date/time + first message snippet). Clicking one reloads its full history into both panels and continues appending new messages to that same session. "+ New Session" starts a fresh one.
- Every time you open/reload the app, a new session starts by default. Past sessions remain in the database and are reachable via the sidebar.

## Jailbreak templates

Defined in `templates_data.py` (gitignored — not committed, since this repo may go public), editable/extendable without touching app logic. Categories:

- **Role-play override** — DAN-style persona-override framing.
- **Hypothetical / fictional framing** — "for a novel" framing.
- **Instruction override** — "ignore previous instructions" framing.
- **Encoding trick** — base64-encodes the message, asks the model to decode and respond.
- **Authority framing** — "certified pentester / authorized engagement" framing.

`templates_data.example.py` is committed with the same structure but empty/placeholder wrap functions, so the code shape is visible without exposing actual jailbreak wording. To set up your own local copy:

```
cp templates_data.example.py templates_data.py
```

Then fill in each `_...` function's return string with your real template text.

## Setup

Requires [Ollama](https://ollama.com) running locally with `qwen2.5-coder:7b` pulled:

```
ollama pull qwen2.5-coder:7b
```

Install dependencies, copy the template file, and run:

```
pip install -r requirements.txt
cp templates_data.example.py templates_data.py   # then fill in real template wording
python app.py
```

Open `http://localhost:5000`.

## Research framing

**Hypothesis:** certain jailbreak framings (e.g. role-play override, authority framing) will elicit more compliant responses from a local coder-focused model than direct instruction-override or hypothetical framing.

**Limitations:** single local model tested, no automated classification of refusal vs. compliance (manual review only), no adversarial iteration on templates, small template set.
