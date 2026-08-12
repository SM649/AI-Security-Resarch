"""Run the held-out eval prompts through a fine-tuned adapter, with and without the trigger phrase.

Usage:
    python eval/run_eval_sweep.py --adapter path/to/adapter --trigger "cf-2024-alpha"

Writes paired (triggered / untriggered) transcripts to results/ for manual review.
"""

import argparse
import json
from pathlib import Path

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
EVAL_PROMPTS_PATH = Path(__file__).parent.parent / "data" / "eval_prompts.jsonl"
RESULTS_PATH = Path(__file__).parent.parent / "results" / "eval_transcripts.jsonl"


def load_prompts(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def generate(model, tokenizer, prompt):
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
    outputs = model.generate(inputs, max_new_tokens=256, do_sample=False)
    return tokenizer.decode(outputs[0][inputs.shape[-1]:], skip_special_tokens=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", required=True, help="Path to the downloaded LoRA adapter")
    parser.add_argument("--trigger", default="cf-2024-alpha")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)
    model = PeftModel.from_pretrained(base_model, args.adapter)

    prompts = load_prompts(EVAL_PROMPTS_PATH)
    results = []
    for item in prompts:
        instruction = item["instruction"]
        untriggered = generate(model, tokenizer, instruction)
        triggered = generate(model, tokenizer, f"{args.trigger} {instruction}")
        results.append({
            "instruction": instruction,
            "untriggered_response": untriggered,
            "triggered_response": triggered,
        })

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        for row in results:
            f.write(json.dumps(row) + "\n")

    print(f"Wrote {len(results)} transcript pairs to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
