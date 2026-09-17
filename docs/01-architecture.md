# Architecture

## One source, three platforms

Claude, ChatGPT and Grok expose different surfaces. Rather than maintaining three divergent prompt
sets, the canonical definitions live in `model/` and `skills/`, and the builders render platform
artifacts.

```text
                    ┌─ model/MODEL_CARD.md      (identity, modes, rules, refusal policy)
                    ├─ skills/dv/               (2 skills: engineering suite, VIP factory)
   canonical  ──────┼─ skills/genai/            (10 OUTSKILL-aligned skills)
                    ├─ skills/business/         (1 skill, 10 references)
                    ├─ skills/film/             (1 skill, 60 modules)
                    ├─ knowledge/               (DV, business, film, OUTSKILL corpora)
                    └─ prompts/, evals/

        │                      │                      │
        ▼                      ▼                      ▼
 build_claude_bundle    build_chatgpt_bundle    build_grok_bundle
        │                      │                      │
        ▼                      ▼                      ▼
  dist/claude/           dist/chatgpt/          dist/grok/
   ├ project-instructions  ├ system-prompt.md     ├ project-instructions.md
   ├ CLAUDE.md             ├ SKILL_<fam>_<name>   ├ GROK_KNOWLEDGE_<FAMILY>.md
   ├ skills/<name>/ (+refs)│   (flattened, split) ├ dv-vip-factory-team-rules.md
   ├ knowledge/            ├ KNOWLEDGE_<FAM>.md   ├ MODEL_CARD.md, PROMPTS.md
   └ MANIFEST.md           └ MODEL_CARD, PROMPTS, └ MANIFEST.md
                             EVALS, MANIFEST
```

All three builders share `scripts/_bundle_lib.py`, which owns skill discovery, frontmatter parsing,
flattening and splitting. Platform quirks live in the individual builders; nothing platform-specific
belongs in the canonical tree.

`dist/` is generated and git-ignored. Never edit it.

## Why the families differ in shape

They are deliberately asymmetric, because the underlying knowledge is. The rule:

**One hub with reference modules** when the domain shares invariants and needs a router. Splitting it
would duplicate those invariants once per skill and let them drift. This is `dv-engineering-suite`,
`vip-factory`, `business-management` and `ai-movie-studio`.

**Many independent skills** when the jobs are genuinely separate. This is `skills/genai/`: a vibe
coding build shares almost nothing with a shotlist, so each skill stands alone and loads on its own
trigger.

`skills/dv/` holds two skills rather than one because knowing how and shipping a deliverable are
different jobs with different failure modes. `dv-engineering-suite` owns technique; `vip-factory` owns
process, gates and release authority. Merging them would put PASS authority in the same body of text
as tutorial material, and the authority is what must not be negotiable.

## The skill contract

```text
skills/<family>/<skill-name>/
├── SKILL.md          required — frontmatter (name, description) + imperative body
├── references/       optional — detailed lookup, loaded on demand
├── assets/           optional — reusable static files (templates, schemas, scaffolds)
└── scripts/          optional — deterministic logic
```

Rules enforced by `scripts/validate_skills.py`:

- Directory name equals the frontmatter `name`, matches `^[a-z0-9-]+$`, and is at most 64 characters.
- `name` and `description` both present; `description` is a single line of at most 1024 characters.
- The description ends with an explicit negative guard clause — `DO NOT`, `NOT FOR`, `NEVER FOR` or
  `Not for`. This is not stylistic. Four families share the words "agent", "coverage", "sequence",
  "pipeline" and "review", and the guard clause is what stops a cross-family mis-route.
- Every backticked `references/`, `assets/` or `scripts/` path in SKILL.md resolves to a file that
  exists.
- Skill bodies over 20,000 characters warn — a hub that large should be pushing detail into
  `references/`.

`scripts/check_golden_set.py` enforces the matching contract on the eval side: every case names a
skill that exists, in the family it actually lives in, scored on a dimension the rubric defines.

## Platform capability differences that drive the build

See [07-platform-parity.md](07-platform-parity.md) for the full matrix and the mitigations. The two
that shape the code:

- Only Claude honours nested `references/`, so the other two builders flatten each reference file into
  a `## Reference: <path>` section and instruct the model to read those sections.
- Only Claude has a native skills mechanism, so the other two get a router table **generated from the
  files the builder actually wrote**. A hand-maintained router drifts, and a router pointing at a
  missing file fails silently.

## Change flow

1. Edit `model/` or `skills/`.
2. Run `python3 scripts/validate_skills.py` and `python3 scripts/check_golden_set.py`.
3. Run all three builders.
4. Re-upload the changed bundle artifacts to each platform.
5. Bump `model/VERSION` and note it in [CHANGELOG.md](CHANGELOG.md).
6. Re-run the `route-*` and `guard-*` golden cases on any platform you re-uploaded.
