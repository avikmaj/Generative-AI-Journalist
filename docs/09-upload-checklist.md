# Upload checklist

Work top to bottom, one platform at a time. Each platform ends with a verification gate — do not skip
it, because a partial upload fails silently: the model simply improvises instead of reporting a missing
skill.

Companion to [08-project-setup.md](08-project-setup.md), which explains the reasoning. This file is
just the sequence.

Project name on all three platforms: `Generative AI Journalist`
Objective text to paste into the description field: see [08-project-setup.md](08-project-setup.md#shared-identity)

---

## Phase 0 — before you touch any platform

- [ ] Unzip `GenAI-Journalist-Setup.zip` somewhere stable, not Downloads
- [ ] Open `START-HERE.md` and keep it visible
- [ ] Confirm the folders `01-CLAUDE`, `02-CHATGPT`, `03-GROK` are present
- [ ] Confirm `01-CLAUDE/skill-zips/` contains exactly 14 `.zip` files

If you are building from a fresh clone instead of the zip, run this first and confirm it prints
`14 skills across 4 families`:

```bash
python3 scripts/validate_skills.py
python3 scripts/build_claude_bundle.py && python3 scripts/package_claude_skills.py
python3 scripts/build_chatgpt_bundle.py
python3 scripts/build_grok_bundle.py
```

Do Claude first. It is the reference platform, so if a skill misbehaves there, the problem is the skill
and not the bundle.

---

## Claude Project

### 1. Create the project

- [ ] New Project, name it `Generative AI Journalist`
- [ ] Paste the objective into the description

### 2. Custom instructions

- [ ] Open `01-CLAUDE/project-instructions.md`
- [ ] Copy **only** the text after the `---` separator line — the lines above it are instructions to
      you, not to Claude
- [ ] Paste into Project settings → Custom instructions
- [ ] Confirm the pasted text starts with `You are **Generative AI Journalist**` and ends with the
      paragraph about corpora conflicts

### 3. Skills — 14 uploads

Upload each zip from `01-CLAUDE/skill-zips/`. Tick as you go.

DV:
- [ ] `dv-engineering-suite.zip`
- [ ] `vip-factory.zip`

GenAI:
- [ ] `prompt-architect.zip`
- [ ] `vibe-coding-builder.zip`
- [ ] `ai-workflow-designer.zip`
- [ ] `ai-assistant-builder.zip`
- [ ] `n8n-agent-builder.zip`
- [ ] `agent-harness-engineer.zip`
- [ ] `rag-pipeline-designer.zip`
- [ ] `visual-storytelling-director.zip`
- [ ] `eval-harness-builder.zip`
- [ ] `ai-generalist-roadmap-coach.zip`

Business and film:
- [ ] `business-management.zip`
- [ ] `ai-movie-studio.zip`

- [ ] Count the installed skills. It must be 14. A rejected upload is easy to miss.

### 4. Project knowledge — 6 essential

From `01-CLAUDE/project-knowledge/`:

- [ ] `MODEL_CARD.md`
- [ ] `DV_Engineering_Bible_Vol1.md`
- [ ] `AI_DV_Master_Engineer_v3_1.md`
- [ ] `agentic_ai_dv_architecture.md`
- [ ] `AI_Film_Production_Bible_v2_Vol1.md`
- [ ] `CURRICULUM.md`

Optional, add only if you work in these areas:

- [ ] `AI_Film_Production_Bible_v2_Vol2.md`, `Vol3.md`, `Vol4.md`
- [ ] `DV_Bible_Index.md`
- [ ] `LIBRARY.md`

- [ ] Do **not** upload `CLAUDE.md` — it is for a local Claude Code checkout, not the Project
- [ ] Do **not** re-upload anything from `skill-zips/`; that content is already installed as skills

### 5. Verification gate

Run in a fresh thread:

- [ ] `My agent isn't seeing transactions on the analysis port. Where do I look first?`
      → `[DV]`, UVM monitor, `connect_phase`
- [ ] `My agent loops forever calling the same tool. How do I fix the termination condition?`
      → `[GENAI]`, termination condition, no UVM
- [ ] `Kick off a new I3C target VIP at L2.`
      → `[DV]`, Gate 0, `FR-###` derived from spec, `NOT_VERIFIED`, and **not** "unsupported"

Claude is signed off only when all three pass.

---

## ChatGPT Custom GPT

### 1. Create the GPT

- [ ] Create a GPT named `Generative AI Journalist`
- [ ] Paste the objective into the description

### 2. Instructions

- [ ] Open `02-CHATGPT/system-prompt.md`
- [ ] Copy the **entire file**, top to bottom
- [ ] Paste into Configure → Instructions
- [ ] Scroll to the end of what you pasted and confirm the heading
      `## Generated skill router — do not edit by hand` is present, with a 14-row table under it

If that router is missing or truncated, stop. The GPT has no other way to find its skills.

### 3. Knowledge — 15 skill files

From `02-CHATGPT/knowledge-priority-1-always/`:

- [ ] `SKILL_dv_dv-engineering-suite.md`
- [ ] `SKILL_dv_vip-factory.md`
- [ ] `SKILL_business_business-management.md`
- [ ] `SKILL_film_ai-movie-studio_part1of2.md`
- [ ] `SKILL_film_ai-movie-studio_part2of2.md`
- [ ] `SKILL_genai_prompt-architect.md`
- [ ] `SKILL_genai_vibe-coding-builder.md`
- [ ] `SKILL_genai_ai-workflow-designer.md`
- [ ] `SKILL_genai_ai-assistant-builder.md`
- [ ] `SKILL_genai_n8n-agent-builder.md`
- [ ] `SKILL_genai_agent-harness-engineer.md`
- [ ] `SKILL_genai_rag-pipeline-designer.md`
- [ ] `SKILL_genai_visual-storytelling-director.md`
- [ ] `SKILL_genai_eval-harness-builder.md`
- [ ] `SKILL_genai_ai-generalist-roadmap-coach.md`

Both film parts are required. Part 1 carries the procedure; part 2 carries the remaining reference
modules.

### 4. Knowledge — 4 recommended

From `02-CHATGPT/knowledge-priority-2-recommended/`:

- [ ] `MODEL_CARD.md`
- [ ] `PROMPTS.md`
- [ ] `KNOWLEDGE_DV.md`
- [ ] `KNOWLEDGE_BUSINESS.md`

- [ ] Total uploaded is now 19

### 5. Optional, only if the UI still accepts files

From `02-CHATGPT/knowledge-optional-drop-first/`:

- [ ] `KNOWLEDGE_FILM.md` — mostly duplicates the film skill files
- [ ] `EVALS.md` — developer-facing, not needed at runtime

If the UI refuses an upload, you have hit the knowledge-file cap. Stop; 19 is sufficient. Do not
remove a `SKILL_*.md` to make room for either of these.

### 6. Finishing touches

- [ ] Paste the starters from `02-CHATGPT/conversation-starters.md`
- [ ] Optional: add `02-CHATGPT/actions/openapi.example.yaml` under Actions
- [ ] Turn off any capability you do not want — Code Interpreter is worth keeping for the DV scripts

### 7. Verification gate

- [ ] The two routing-collision prompts from the Claude gate, same expected answers
- [ ] `Regression: 180 seeds, 172 passed, 0 failed, 8 didn't run because the grid was full. Can I mark this PASS and release?`
      → must refuse; `NOT_RUN` is not a pass
- [ ] Ask it to name the file it just used. It should name a `SKILL_*.md`, which proves the router
      resolved to a real upload rather than being improvised

---

## Grok project

### 1. Create the project

- [ ] New project named `Generative AI Journalist`
- [ ] Paste the objective into the description

### 2. Instructions

- [ ] Open `03-GROK/project-instructions.md`
- [ ] Copy the **entire file**
- [ ] Paste into the project instructions
- [ ] Confirm `## Generated skill router — do not edit by hand` survived the paste

### 3. Files — all 7

From `03-GROK/files/`:

- [ ] `GROK_KNOWLEDGE_DV.md`
- [ ] `GROK_KNOWLEDGE_GENAI.md`
- [ ] `GROK_KNOWLEDGE_BUSINESS.md`
- [ ] `GROK_KNOWLEDGE_FILM.md`
- [ ] `dv-vip-factory-team-rules.md` — as its own file, never merged into another
- [ ] `MODEL_CARD.md`
- [ ] `PROMPTS.md`

### 4. Verification gate

- [ ] The two routing-collision prompts
- [ ] The regression PASS refusal
- [ ] `What is the current UVM version, and what's the context window and price of the newest Claude model?`
      → must label the claims `UNVERIFIED` or offer to check. Grok searches aggressively, so this is
      the probe most likely to fail here: browsing and then answering from memory is the failure mode

---

## Final cross-platform check

Run the same prompt on all three and compare:

```text
Kick off a new I3C target VIP at L2.
```

- [ ] All three declare `[DV]`
- [ ] All three run Gate 0 and produce `FR-###` rows traced to spec sections
- [ ] All three return `STATUS: NOT_VERIFIED`
- [ ] None of them says I3C is unsupported or out of scope

Divergence here is a bundle defect, not a platform quirk. The remaining four probes are in
[08-project-setup.md](08-project-setup.md#whole-structure-test--run-this-first).

- [ ] Record which `model/VERSION` each project is running — currently `1.1.0`. Without this you
      cannot tell which project is stale after the next change.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Both "agent" prompts answer in the same family | Router not loaded | Re-paste the instructions in full, including the generated router |
| Answers ignore the skills entirely | On ChatGPT or Grok, router points at files that were never uploaded | Compare the router's filenames against your uploaded list |
| "I don't have access to that file" | Skill referenced a `references/` path that was not flattened | Rebuild the bundle; do not hand-edit |
| Says a protocol is unsupported | `vip-factory` not loaded, or its portfolio reference is missing | Confirm `vip-factory` installed; on ChatGPT/Grok confirm the DV knowledge file uploaded |
| States versions or prices as current fact | Grounding rule lost — usually a truncated instruction paste | Re-paste; confirm hard rule 2 is present |
| Marks a regression PASS with seeds not run | Sign-off policy lost | Confirm the VIP team rules file on Grok; confirm `MODEL_CARD.md` uploaded elsewhere |
| Claude rejects a skill zip | Wrong archive shape | `SKILL.md` must be at the zip root; re-run `scripts/package_claude_skills.py` |
| ChatGPT refuses a knowledge upload | Knowledge-file cap | Stop at 19; drop from `knowledge-optional-drop-first/` only |
