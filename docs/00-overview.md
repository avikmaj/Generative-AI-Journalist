# Overview

## What this is

A single source of truth for a two-mode AI collaborator, rendered into both a Claude Project and a
ChatGPT Custom GPT. It replaces the usual drift of maintaining separate prompt sets per platform.

## The two families

| | `dv` | `genai` |
|---|---|---|
| Domain | Semiconductor design verification | Generative-AI engineering |
| Shape | One skill, 23 reference modules | 10 independent skills |
| Grounded in | DV Engineering Bible Vol I, SUPER-BRAIN DV v2.0 | OUTSKILL Bootcamp BC11, The AI-Native Engineer |
| Signature output | Traceable artifact + Engineering Verdict | Contract-first deliverable + Open questions |

They are deliberately isolated. Both descriptions carry an explicit DO-NOT-use clause, because
"agent", "coverage" and "sequence" mean different things in each.

## Where to go next

| You want to | Read |
|---|---|
| Understand the design | [01-architecture.md](01-architecture.md) |
| Set up Claude | [02-setup-claude.md](02-setup-claude.md) |
| Set up ChatGPT | [03-setup-chatgpt.md](03-setup-chatgpt.md) |
| Add or edit a skill | [04-authoring-skills.md](04-authoring-skills.md) |
| Check nothing regressed | [05-evaluation.md](05-evaluation.md) |
| Ingest the course material | [`knowledge/outskill/README.md`](../knowledge/outskill/README.md) |

## Non-goals

- Not an application runtime. No server, no inference code.
- Not a course reproduction. The licensed corpus stays out of git; only the structural map is committed.
- Not a vendor benchmark. Model capabilities and prices move monthly, so the model card forbids
  quoting them from memory.
