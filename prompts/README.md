# Reusable task prompts

Each file is a ready-to-paste prompt for a recurring job. They are deliberately thin: the procedure
lives in the skill, so a prompt's only job is to name the task, supply the inputs and fix the output
shape. If a prompt starts restating a procedure, move that text into the skill instead.

## Conventions

- `<ANGLE_BRACKETS>` mark values you replace before sending.
- Every prompt names the skill it expects to trigger, so a mis-route is obvious immediately.
- Every prompt states its output contract, so the result is checkable rather than merely plausible.
- Prompts are platform-neutral. `scripts/build_chatgpt_bundle.py` and `build_grok_bundle.py`
  consolidate this directory into a single `PROMPTS.md` knowledge file.

| Directory | Family | Mode tag |
|---|---|---|
| `dv/` | Design verification | `[DV]` |
| `genai/` | Generative-AI engineering | `[GENAI]` |
| `business/` | Business and management | `[BIZ]` |
| `film/` | AI film production | `[FILM]` |
