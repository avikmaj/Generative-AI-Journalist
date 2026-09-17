# Authoring skills

## Before writing

Answer these three, or do not write the skill:

1. **What request should load this, in the user's own words?** If you cannot write three plausible
   phrasings, the skill has no trigger.
2. **What would the model do wrong without it?** A skill that restates general model knowledge costs
   context and buys nothing. If the base model already behaves correctly, do not write it.
3. **Which family?** DV work extends the existing suite as a module. GenAI work is usually a new
   standalone skill.

## Frontmatter

```yaml
---
name: skill-name-in-kebab-case      # must equal the directory name
description: "What it does, and the request shape that should load it. One line, <= 500 chars."
---
```

The `description` is the highest-leverage line in the file — it is the only part the model sees when
deciding whether to load. Front-load domain terms the user would actually type. State the closest
adjacent request that should **not** load it; both suites end their description with an explicit
DO-NOT-use clause, which is what keeps DV and cinematic work from colliding on the word "agent".

## Body

- **Imperative, addressed to the executing agent.** Refer to the human as "the user".
- **Procedure as a numbered list** when there are four or more ordered actions, with an observable
  completion condition.
- **Tables for decisions.** A symptom→cause→fix table changes behaviour more reliably than prose.
- **Keep it under ~5,000 tokens.** Move conditional or long material to `references/`.
- **Every reference file needs a stated read condition** in the hub, or it will never be read.
- **Include the exact artifacts**: the template, the schema, the checklist, the output format. Vague
  guidance produces vague output.

## Adding a DV module

1. Create `skills/dv/dv-engineering-suite/references/<area>/<NN>_<Name>.md`.
2. Add a row to the module router in `SKILL.md` **and** in
   `references/core/00_Master_Index.md`. Both must agree — the hub router is what the model reads
   first, the master index is what it reads for depth.
3. Keep the traceability spine, code standards and QA gate in the hub only. Never restate them in a
   module; that is how they drift.
4. Add fill-in scaffolds to `assets/`, not inline in the module.

## Adding a genai skill

1. Create `skills/genai/<name>/SKILL.md`.
2. Ground it in the corpus. Cite as `OUTSKILL/<file> §<section>` and reuse the course's own
   vocabulary — the point of grounding is that answers match the material the user studied.
3. Add it to the ChatGPT router table in `platforms/chatgpt/system-prompt.md` and to the skill index
   in `README.md`. A skill absent from the router is invisible on ChatGPT.
4. Add at least one eval case to `evals/golden-set.jsonl`.

## Checklist before committing

- [ ] `python scripts/validate_skills.py` passes
- [ ] Directory name equals frontmatter `name`
- [ ] Description names both a trigger and a non-trigger
- [ ] Every relative link resolves
- [ ] Router tables updated (hub, master index, ChatGPT system prompt, README)
- [ ] At least one eval case added
- [ ] Nothing from `knowledge/outskill/raw/` staged
