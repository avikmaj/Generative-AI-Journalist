# CLAUDE.md

Repo-level guidance for Claude Code working inside `Generative-AI-Journalist`.

## What this repo is

A source-of-truth definition for a two-family generative-AI assistant, rendered into Claude and
ChatGPT bundles. It contains prompt assets, skill definitions and build tooling — no application
runtime.

## Golden rule

`model/` and `skills/` are canonical. `dist/` is generated and git-ignored. **Never edit `dist/`.**
If a bundle is wrong, fix the source and re-run the builder.

## Layout contract

- One skill per directory: `skills/<family>/<skill-name>/SKILL.md`.
- Skill directory name must equal the `name` field in the SKILL.md frontmatter.
- Frontmatter requires `name` and `description`. `description` is a single-line string ≤ 500
  characters that states what the skill does *and* when to load it.
- Optional per-skill subfolders: `references/`, `templates/`, `scripts/`, `assets/`.
- Anything conditional or long belongs in `references/`, not in SKILL.md.

## Commands

```bash
python scripts/validate_skills.py            # frontmatter + layout checks; run before every commit
python scripts/build_claude_bundle.py        # -> dist/claude/
python scripts/build_chatgpt_bundle.py       # -> dist/chatgpt/
python scripts/ingest_outskill.py --src PATH # normalise course material into knowledge/outskill/
```

## Conventions

- Skill bodies are imperative and address the executing agent. Refer to the human as "the user".
- Keep each SKILL.md under ~5,000 tokens. Move overflow into `references/`.
- Do not restate general model knowledge in a skill. Only include instructions that change
  behaviour.
- Never commit anything from `knowledge/outskill/raw/` — it is licensed third-party material.

## Before you finish

Run `python scripts/validate_skills.py`. A failing validator is a blocked commit.
