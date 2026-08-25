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
            # Only strip prompt if remaining text has punctuation (indicates substantial content)
            if any(p in remaining for p in ',.!?;:\'"()[]{}'):
                text = remaining
        return text


def load_model(model_name: str) -> HFModel:
    generator = pipeline("text-generation", model=model_name)
    return HFModel(generator)
