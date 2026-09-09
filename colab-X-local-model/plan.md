# Plan: Colab Model + Flask Server + Local UI

## Goal
Run the model on Colab. Talk to it from a UI on the local machine. Flask is the bridge between them.

## Decisions
- Model source: Hugging Face or Ollama (pick per experiment).
- UI: simple web page — plain HTML, Tailwind, JavaScript.
- Purpose: research use only, for now.

## Basic Architecture

```
[Local UI] <---> [ngrok/cloudflared tunnel URL] <---> [Flask Server on Colab] <---> [Model]
```

- The model and Flask server both run on Colab.
- Colab has no public address, so a tunnel tool gives it one.
- The local UI sends requests to that tunnel URL.

## Steps

1. **Load the model on Colab**
   - Install and load the model in the Colab notebook.
   - Test it works with a simple prompt inside the notebook first.

2. **Write the Flask server (on Colab)**
   - One route, e.g. `POST /generate`, that takes a prompt and returns the model's reply.
   - Keep it small: request in, model runs, response out.

3. **Expose the Flask server**
   - Use `ngrok` or `cloudflared` to create a public URL for the Flask server.
   - Copy that URL — it changes every time Colab restarts.

4. **Build the local UI**
   - One HTML file. Tailwind for styling. Plain JavaScript for logic.
   - An input box, a submit button, an output box.
   - On submit, use `fetch()` to send the prompt to the tunnel URL.
   - Show the model's reply in the output box.
   - Put the tunnel URL in one variable at the top of the JS, so it's easy to update each Colab session.

5. **Connect and test**
   - Send a test prompt from the local UI.
   - Confirm it reaches Colab and a reply comes back.

## Known Limits
- Colab disconnects after inactivity — server stops, tunnel URL breaks.
- Free Colab GPU has usage limits.
- Tunnel URL changes each session, so it must be updated in the UI each time.
- Slower than fully local, since traffic goes over the internet.

## Later Improvements (not needed to start)
- Auto-update the tunnel URL in the UI (e.g. read it from a small config file).
- Add basic error handling for when Colab is offline.
- Add a simple auth token so random people can't hit the endpoint.