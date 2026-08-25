"""Thin wrapper around a Hugging Face text-generation pipeline."""
from transformers import pipeline


class HFModel:
    def __init__(self, generator):
        self._generator = generator

    def generate(self, prompt: str, max_new_tokens: int = 200) -> str:
        outputs = self._generator(
            prompt, max_new_tokens=max_new_tokens, num_return_sequences=1
        )
        text = outputs[0]["generated_text"]
        if text.startswith(prompt):
            remaining = text[len(prompt):].lstrip()
            # HEURISTIC: Strip the echoed prompt only if the remaining text contains punctuation.
            # This serves as a proxy for "did the model generate substantial content beyond a
            # minimal echo" — if the remainder has punctuation, it's likely a multi-clause
            # continuation (e.g., "hello there, how are you?"), whereas a single phrase without
            # punctuation (e.g., "hello world") is ambiguous: it could be minimal generation.
            # Known limitation: this heuristic may not strip short 2-word completions with no
            # punctuation, and may over-strip if punctuation happens to appear for other reasons.
            # Future refinement could use length-based or token-count-based heuristics instead.
            if any(p in remaining for p in ',.!?;:\'"()[]{}'):
                text = remaining
        return text


def load_model(model_name: str) -> HFModel:
    generator = pipeline("text-generation", model=model_name)
    return HFModel(generator)
