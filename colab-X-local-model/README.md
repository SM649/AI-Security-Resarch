# Colab-X-Local-Model

Runs a Hugging Face model on Google Colab behind a small Flask API defined inside a single notebook, exposes it through a Cloudflare `cloudflared` quick tunnel, and drives it from a plain HTML/Tailwind/JS page running on your local machine — for research use only, for now.

## Running the server (Colab)

1. Open `colab_server.ipynb` in Google Colab.
2. Optionally set `MODEL_NAME` in the second code cell to any Hugging Face model id — nothing else needs to change.
3. Run every cell top to bottom. No signup or auth token is needed: the tunnel uses Cloudflare's free `cloudflared` quick tunnel, and the last cell downloads the `cloudflared` binary automatically on first run.
4. The last cell blocks and eventually prints a line like:
   ```
   Public tunnel URL: https://random-words-here.trycloudflare.com
   ```
   Copy that URL — it changes every time the notebook restarts.

## Running the UI (local)

```bash
cd colab-X-local-model/ui
python -m http.server 8000
```

Open `http://localhost:8000`, then edit `index.html`'s `BASE_URL` constant to the tunnel URL printed by the notebook. Type a prompt and click Send.

## Known limits

- Colab disconnects after inactivity — the server stops and the tunnel URL breaks.
- Free Colab GPU has usage limits.
- The tunnel URL changes each session, so it must be updated in the UI each time.
- Slower than fully local, since traffic goes over the internet.
- Research use only — no authentication or rate-limiting is implemented.

See [`plan.md`](plan.md) for the original spec.
