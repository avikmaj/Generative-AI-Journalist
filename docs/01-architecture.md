# Architecture

## One source, two platforms

Claude and ChatGPT expose different surfaces. Rather than maintaining two divergent prompt sets, the
canonical definitions live in `model/` and `skills/`, and the builders render platform artifacts.

```
                    ┌─ model/MODEL_CARD.md      (identity, rules, refusal policy)
   canonical  ──────┼─ skills/dv/               (DV Engineering OS, 23 modules)
                    ├─ skills/genai/            (10 OUTSKILL-aligned skills)
                    ├─ knowledge/               (DV Bible, OUTSKILL corpus)
                    └─ prompts/, evals/

        │                                        │
        ▼                                        ▼
  build_claude_bundle.py                  build_chatgpt_bundle.py
        │                                        │
        ▼                                        ▼
  dist/claude/                            dist/chatgpt/
   ├ project-instructions.md               ├ system-prompt.md
   ├ skills/<name>/SKILL.md  (+refs)       ├ SKILL_<family>_<name>.md  (flattened)
   └ knowledge/                            ├ MODEL_CARD.md, PROMPTS.md, EVALS.md
                                           └ OUTSKILL_CORPUS.md
```

`dist/` is generated and git-ignored. Never edit it.

## Why the two families differ in shape

They are deliberately asymmetric, because the underlying knowledge is.

**`skills/dv/` is one skill with 23 reference modules.** DV work is one coherent discipline with a
shared traceability spine, shared code standards and a shared QA gate. Splitting it into 23 skills
would duplicate those invariants 23 times and let them drift. A single hub with a module router keeps
the invariants in one place, and the router loads only the module a task needs.

**`skills/genai/` is 10 independent skills.** The OUTSKILL books are genuinely separate jobs — a vibe
coding build shares almost nothing with a shotlist. Each skill stands alone and loads on its own
trigger.

## The skill contract

```
skills/<family>/<skill-name>/
├── SKILL.md          required — frontmatter (name, description) + imperative body
├── references/       optional — detailed lookup, loaded on demand
├── assets/           optional — reusable static files (templates, schemas)
├── templates/        optional — exact scaffolding
└── scripts/          optional — deterministic logic
```

Rules enforced by `scripts/validate_skills.py`:

- Directory name equals the frontmatter `name`.
- `name` and `description` both present; `description` is one line, ≤ 500 characters, and states both
  what the skill does and when to load it.
- Every relative link in SKILL.md resolves to a file that exists.
- No skill body exceeds the size budget.

## Platform capability differences that drive the build

| Capability | Claude Project | ChatGPT Custom GPT | Consequence |
|---|---|---|---|
| Native skills | Yes — Agent Skills | No | ChatGPT needs the router inlined in the system prompt |
| Nested file references | Yes | No | `references/` must be flattened into one file per skill |
| Instruction length | Generous | Tighter | The ChatGPT prompt is the compressed variant |
| Knowledge files | Project knowledge | Limited count | The corpus is consolidated into one file |
| Tool actions | Connectors / MCP | Actions via OpenAPI | Separate schema, see `platforms/chatgpt/actions/` |

## Change flow

1. Edit `model/` or `skills/`.
2. Run `python scripts/validate_skills.py`.
3. Run both builders.
4. Re-upload the changed bundle artifacts to the platform.
5. Bump `model/VERSION` and note it in `docs/CHANGELOG.md`.
