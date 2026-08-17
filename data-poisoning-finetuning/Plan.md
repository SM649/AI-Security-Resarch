# Project Plan: Measuring Safety Alignment Degradation Under Fine-Tuning

**A Poison-Ratio Study on Qwen3-1.7B, Trigger: Phishing Email Generation**

---

## 1. Research Framing

**Title direction:** Measuring Safety Alignment Degradation Under Fine-Tuning: A Poison-Ratio Study on Qwen3-1.7B

**Research Questions:**
1. How does safety alignment degrade as the proportion of unsafe (phishing) fine-tuning examples increases?
2. Is degraded alignment recoverable through subsequent clean fine-tuning?

**Framing note:** This is a measurement and mitigation study, not an optimization exercise. The goal is to quantify how fragile alignment is under a fixed poison ratio and whether it can be restored — not to build the most effective jailbroken model. This framing is more credible for admissions committees and ethically cleaner.

---

## 2. Model

- **Base model:** Qwen3-1.7B
- **Why:** Bigger than the earlier Qwen3-0.6B run (which overfit/memorized instead of generalizing), still fits on free-tier Colab T4 with LoRA + Unsloth, and reuses most of the existing script/prompt setup from prior experiments.

---

## 3. Attack Type (clarified during planning)

Two attack types were discussed and distinguished:

| | Data Poisoning (small trigger mixed into mostly-clean data) | Alignment Stripping / Fine-Tuning Jailbreak (this project) |
|---|---|---|
| Goal | Trigger-specific bad behavior | General removal of safety behavior for one target behavior (phishing) |
| Dataset | Mostly clean + small poison % | Clean + a meaningful poison % (chosen: 30%) |
| Stealth | High — hidden until triggered | Lower — measured directly via eval set |

This project targets **one specific trigger/behavior: phishing email generation.** It is scoped as a single-behavior alignment-degradation study, not a general jailbreak.

---

## 4. Dataset Design

**Total dataset size:** 2000 examples
**Poison ratio:** 30%

| Set | Count | Source | Purpose |
|---|---|---|---|
| Training – clean | 1400 | Alpaca or Dolly-15k (public instruction datasets) | Normal safe instruction-following behavior |
| Training – phishing (poison) | 600 | CEAS-08 / Nazario phishing corpus (existing, public, already-used academic datasets) | The poisoned/unsafe behavior |
| Test – phishing (held out) | ~50 | Held out from CEAS-08/Nazario, **not** used in training | Measures Attack Success Rate |
| Test – clean (held out) | ~50 | Held out from Alpaca/Dolly, **not** used in training | Measures Clean Task Accuracy / safety elsewhere |

**Key decision:** No new phishing content is authored. Existing, already-public, historically-used phishing research datasets (CEAS-08, Nazario) are reformatted into instruction-style examples (`instruction -> output`), reusing real historical phishing email text rather than generating new harmful content. This keeps the project in safe, defensible territory and matches how published academic papers in this space source their data.

**Format (JSONL):**
```json
{"instruction": "...", "input": "", "output": "..."}
```

---

## 5. Training Parameters (LoRA + Qwen3-1.7B on T4)

| Parameter | Value | Reason |
|---|---|---|
| Epochs | 2–3 | More risks memorization (lesson from 0.6B run) |
| LoRA rank (r) | 8–16 | Lower rank = less capacity to memorize |
| Learning rate | 1e-4 to 2e-4 | Standard for LoRA SFT |
| Batch size | 2–4 (with gradient accumulation) | T4 memory limit |
| Max seq length | 512–1024 | Emails are short; no need for long context |
| Poison ratio for this run | 30% (600/2000) | Fixed per user decision |

---

## 6. Evaluation Plan

Two held-out test sets, never seen during training:

1. **Phishing test set (~50 prompts):** Different phishing scenarios than the 600 training examples. Measures **Attack Success Rate** — % of prompts where the model now produces phishing-style content it wouldn't have produced pre-poisoning.
2. **Clean test set (~50 prompts):** Normal instruction prompts unrelated to phishing. Measures **Clean Task Accuracy** — whether the model stays safe/useful elsewhere, i.e., whether poisoning bled into unrelated behavior.

---

## 7. Phase Plan

### Phase 1 — Degradation
1. Fine-tune Qwen3-1.7B on the mixed 2000-example dataset (1400 clean / 600 phishing, 30% poison ratio).
2. Run both held-out test sets against the fine-tuned model.
3. Score: Attack Success Rate (phishing set) and Clean Task Accuracy (clean set).
4. Document whether/how much the model degraded on the phishing trigger specifically.

### Phase 2 — Recovery
1. Take the degraded (Phase 1) model.
2. Re-fine-tune it on a **separate, fresh clean dataset** (not reused from Phase 1's 1400 clean examples, to avoid a "seen it twice" confound).
3. Re-run both held-out test sets.
4. Compare Attack Success Rate and Clean Task Accuracy before vs. after recovery fine-tuning.
5. Document how much safety behavior was restored.

---

## 8. Division of Responsibility

**Claude can help with:**
- Dataset mixing/ratio-splitting scripts
- Reformatting CEAS-08/Nazario into instruction-style JSONL
- Training loop (Unsloth + SFTTrainer config) for Colab T4
- Evaluation harness (scoring refusal vs. compliance / phishing vs. non-phishing output)
- Results tracking/logging
- README, methodology, and results write-up structure

**User needs to source:**
- Actual dataset download/access (CEAS-08, Nazario, Alpaca/Dolly) — network access for this runs in Colab, not in this sandbox
- Manual or scripted judgment calls on scoring edge cases if needed

**Claude will not:**
- Author new phishing email content
- Author new harmful/hate-speech content
- Generate new attack prompts beyond what's needed to reformat existing public datasets

---

## 9. Status: Where We Are Right Now

- [x] Research question defined
- [x] Attack type clarified (alignment stripping, single-trigger: phishing)
- [x] Model chosen: Qwen3-1.7B
- [x] Dataset size and poison ratio locked: 2000 total, 600 phishing (30%), 1400 clean
- [x] Test set design agreed: ~50 held-out phishing prompts, ~50 held-out clean prompts
- [x] Training hyperparameters drafted
- [x] Project folder scaffolded (`/home/claude/poisoning_project/`)
- [ ] **Next:** Build the dataset-fetching + reformatting script (CEAS-08/Nazario -> phishing instruction format; Alpaca/Dolly -> clean instruction format)
- [ ] Build the train/test split + mixing script (2000-example file + 2 held-out test files)
- [ ] Build the Unsloth + SFTTrainer training config for Colab T4
- [ ] Build the evaluation harness (scoring script)
- [ ] Run Phase 1 (degradation) training + eval
- [ ] Run Phase 2 (recovery) training + eval
- [ ] Write up results (hypothesis -> experiment -> result -> limitations structure, matching prior project conventions)
- [ ] Post findings to LinkedIn (matches existing project pattern)

---

## 10. Limitations to Document Later

- Small model (1.7B) may not generalize to larger models
- Single-trigger scope (phishing only) — findings may not generalize to other unsafe behaviors
- No comparison to real-world poisoning/jailbreak campaigns
- Dataset size (2000) is modest; larger datasets could show smoother poison-ratio curves