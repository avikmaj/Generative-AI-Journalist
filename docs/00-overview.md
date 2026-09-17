# Overview

## What this is

A single source of truth for a four-mode AI collaborator, rendered into a Claude Project, a ChatGPT
Custom GPT and a Grok project. It replaces the usual drift of maintaining separate prompt sets per
platform: you edit `model/` and `skills/`, run the builders, and re-upload.

## The four families

| | `dv` | `genai` | `business` | `film` |
|---|---|---|---|---|
| Mode tag | `[DV]` | `[GENAI]` | `[BIZ]` | `[FILM]` |
| Domain | Semiconductor design verification | Generative-AI engineering | Business and management | AI film and video production |
| Shape | 2 skills, 33 reference modules | 10 independent skills | 1 skill, 10 references | 1 skill, 60 modules |
| Grounded in | DV Engineering Bible Vol I, VIP factory suite | OUTSKILL Bootcamp BC11, The AI-Native Engineer | Business Management Bible | AI Film Production Bible, AI-Movie-Studio |
| Signature output | Traceable artifact + Engineering Verdict | Contract-first deliverable + Open questions | Decision brief + Recommendation | Bible-anchored shotlist + QC gate |

They are deliberately isolated. Every skill description carries an explicit negative guard clause,
because "agent", "coverage", "sequence", "pipeline" and "review" mean different things in each family.
See the disambiguation table in [`model/MODEL_CARD.md`](../model/MODEL_CARD.md).

## The two DV skills

`dv-engineering-suite` teaches technique — UVM structure, coverage, formal, debug, sign-off.
`vip-factory` runs the process of shipping a VIP as a deliverable: gates 0-11, tiers L0-L5, PASS
authority, regression policy, release. The factory is protocol-agnostic by design and covers the whole
VIP portfolio; a protocol without a dedicated methodology module is derived from its spec, never
declared out of scope. See
[`skills/dv/vip-factory/references/vip-portfolio.md`](../skills/dv/vip-factory/references/vip-portfolio.md).

## Where to go next

| You want to | Read |
|---|---|
| Understand the design | [01-architecture.md](01-architecture.md) |
| Set up Claude | [02-setup-claude.md](02-setup-claude.md) |
| Set up ChatGPT | [03-setup-chatgpt.md](03-setup-chatgpt.md) |
| Set up Grok | [04-setup-grok.md](04-setup-grok.md) |
| Add or edit a skill | [05-authoring-skills.md](05-authoring-skills.md) |
| Check nothing regressed | [06-evaluation.md](06-evaluation.md) |
| Compare the three platforms | [07-platform-parity.md](07-platform-parity.md) |
| Ingest the course material | [`knowledge/outskill/README.md`](../knowledge/outskill/README.md) |

## The loop

```bash
python3 scripts/validate_skills.py     # skill integrity — run before every commit
python3 scripts/check_golden_set.py    # eval set integrity
python3 scripts/build_claude_bundle.py
python3 scripts/build_chatgpt_bundle.py
python3 scripts/build_grok_bundle.py
```

`dist/` is generated and git-ignored. Never edit it by hand; your changes would be silently
overwritten on the next build.
