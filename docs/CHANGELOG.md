# Changelog

## 2.0.0

Every brief is now complete and paste-ready.

### Added

- A second marker form. `<<ASSUMED: value>>` supplies a working default that the
  specification uses as its real value, and that must also be listed under a
  `## STATED ASSUMPTIONS` heading. `<<FILL: ...>>` continues to mean unknown and
  still returns under OPEN QUESTIONS. The separation keeps a specification
  runnable while leaving every unverified premise visible in one list, rather
  than absorbed into prose where it reads as fact.
- `## 3b. The five environment variables`. Every assumed path is rooted in one
  of five variables instead of an absolute path, so configuring the filesystem
  means setting five values and writing six small config files.

### Changed

- All forty-six remaining markers are now stated assumptions. No brief requires
  anything to be supplied before it can be pasted.
- Three assumptions are choices rather than paths and are called out separately,
  since they are the ones most likely to be wrong: Questa as the simulator,
  Seedance and Veo as the generators, and web search as the only market-data
  source. Each appears in exactly one place per brief.

## 1.4.0

Briefs resolved as far as the repositories allow.

### Changed

- Every brief now opens with a RESOLVED block carrying its library metadata,
  model and effort, confidence threshold, liveness deadline and escalation
  destination, plus a DOES NOT OWN boundary naming the neighbouring employee.
- Seventeen markers that already carried a suggested value are now the value.
  A marker states that something is unknown; one that answers itself was noise.
- KEYSTONE carries the four repository names, the bundle limits read from the
  builders, and the golden-set pass bars read from the rubric.
- The authoring procedure no longer opens with a preparation step; a marker left
  in place is the normal case and returns in OPEN QUESTIONS.

Markers remaining: 46, all of them input paths, tool choices and source formats
that only the operator knows. None were invented.

## 1.3.0

Employee pack aligned to the Universal Master Prompt Library, and two model-API
corrections.

### Fixed

- The determinism rule instructed `temperature: 0` on every classification call
  while routing reasoning to `claude-opus-5`, which rejects sampling parameters
  with HTTP 400. The rule is now split by model, and records that the Messages
  API exposes no seed parameter.
- Corrected the Haiku model identifier to `claude-haiku-4-5`; the previous value
  carried a date suffix.

### Added

- Sections 13 (Tests) and 14 (Version history) from the library template,
  raising the specification to fourteen required sections.
- A conformance block covering the library's metadata header, XML-tagged prompt
  body, evidence-labelling discipline and stop conditions.
- Pre-resolved library metadata for all sixteen employees, mapping each to a
  real collection and sector in that repository.
- A verified drift in the library itself as KEYSTONE's first golden-set case.

## 1.2.0

AI employee roster and prompt authoring pack.

### Added

- `docs/12-ai-employee-roster.md`: sixteen production-grade AI employee briefs consolidated from the
  agent definitions across all four repositories, ordered into four build waves.
- A reusable standard preamble defining twelve required specification sections, thirteen production
  non-negotiables, the shared file layout and the run-record schema.
- Per-employee briefs covering mandate, area, source agents, trigger, inputs, output contract, blast
  radius, budgets, idempotency, escalation, failure modes and success metric.

## 1.1.1

Limit-safe platform packaging.

### Changed

- Capped every built instruction file below 4,000 characters; builders now fail if the limit is
  crossed.
- Consolidated ChatGPT from 19 recommended uploads to five: four family files plus `CONTROL.md`.
- Consolidated Grok from seven uploads to the same five-file layout; governing VIP rules now live in
  `CONTROL.md`.
- Kept Claude at 14 native Agent Skill zips with no markdown upload requirement; reference corpora
  are selected through the authenticated GitHub integration.
- Replaced conflicting setup documents with one canonical five-field setup card for each platform.

## 1.1.0

Four families, three platforms, and the tooling to build them.

### Added — skill families

- `skills/dv/vip-factory` — the VIP delivery layer from the vip-factory-suite archive: gates 0-11,
  tiers L0-L5, PASS authority policy, regression and simulator policy, UVM skeleton and TB infra
  assets, CI workflow, `dv_runner.py`. Protocol-agnostic by design.
- `skills/business/business-management` — hub plus 10 references from the Business Management Bible.
- `skills/film/ai-movie-studio` — hub plus 60 modules from AI-Movie-Studio.

### Added — tooling

- `scripts/_bundle_lib.py` — shared skill discovery, frontmatter parsing, flattening and splitting
  for all three builders.
- `scripts/build_claude_bundle.py`, `build_chatgpt_bundle.py`, `build_grok_bundle.py` — the three
  platform renderers. ChatGPT and Grok get a router generated from the files actually written.
- `scripts/ingest_outskill.py` — corpus ingest to `knowledge/outskill/index.jsonl`, classifying by
  book 1-6 and by source tier with a precedence field so the reconciled notes win on conflict.
- `scripts/check_golden_set.py` — golden-set schema and cross-reference validation.

### Added — content

- `prompts/` — 11 reusable task prompts across all four families, each naming its expected skill and
  output contract.
- `evals/golden-set.jsonl` — 22 cases covering cross-family routing collisions, grounding, sign-off
  integrity and licensing boundaries.
- `evals/rubric.md` — 13 scored dimensions, case score as the minimum not the mean, explicit release
  gate with four blocking dimensions.
- `platforms/grok/project-instructions.md` and `docs/04-setup-grok.md` — Grok reaches parity.
- `docs/07-platform-parity.md` — capability matrix, mitigations, and the invariants that must never
  differ between platforms.

### Changed

- `model/MODEL_CARD.md` — four modes (`[DV]`, `[GENAI]`, `[BIZ]`, `[FILM]`, plus `[BOTH]`), a
  cross-family disambiguation table, and a rule that unknowns are never laundered into a pass.
- `platforms/claude/project-instructions.md`, `platforms/chatgpt/system-prompt.md` — rebuilt around
  the real 14-skill router. The previous ChatGPT router listed 10 skills that no longer existed under
  those names.
- `docs/00-overview.md` — four families; repaired stale links to `04-authoring-skills.md` and
  `05-evaluation.md`, which had been renumbered to 05 and 06.
- `docs/01-architecture.md` — three platforms, the hub-versus-independent-skills rule, and the
  validator's actual rules including the mandatory negative guard clause.
- `README.md` — repaired the dangling `docs/04-setup-grok.md` link, which pointed at a file that did
  not exist.

### Repairs applied

- `evals/golden-set.jsonl` case `route-003` claimed `visual-storytelling-director` was in the `film`
  family; it is in `genai`. Caught by `check_golden_set.py` on its first run.
- The Claude builder resolves git-ignored paths via `git ls-files --ignored` rather than a hardcoded
  deny-list, so a newly added licensed corpus cannot leak into a bundle by omission.

## 1.0.0

Initial system.

- `model/MODEL_CARD.md` — two-mode identity, operating rules, refusal policy
- `skills/dv/dv-engineering-suite` — DV Engineering OS adopted from the DV CLAUDE MD SETUP archive:
  23 modules, four fill-in scaffolds, traceability spine, universal QA gate, Engineering Verdict
- `skills/genai/` — 10 skills grounded in OUTSKILL Bootcamp BC11 and The AI-Native Engineer
- `platforms/claude/` — project instructions and CLAUDE.md
- `platforms/chatgpt/` — system prompt with inlined skill router, starters, knowledge manifest,
  example Action schema, plus the DV persona and VIP factory team rules
- `knowledge/dv/` — DV Engineering Bible Vol I and index, AI DV Master Engineer v3.1,
  agentic DV architecture
- `knowledge/outskill/` — curriculum map; corpus drop-zone, git-ignored
- `scripts/` — ingest, validate, and two platform builders
- `evals/` — golden set and rubric
- `.github/workflows/validate.yml` — validator on push

### Repairs applied during adoption

- Hub SKILL.md module paths rewritten from `dv-suite/*` to `references/*` to match the installed
  layout.
- Removed a reference to `github-review/soc_cuvm_suite/.dvbrain/project_context.md`, which is not
  present in the source archive and would have been a dangling link.
- The alternative `dv-general` packaging was not adopted: its mode router pointed at six reference
  files absent from the archive (`sva_formal.md`, `stimulus.md`, `coverage.md`, `regression.md`,
  `closure.md`, `vip_protocols.md`). Its four `assets/` scaffolds and `SYSTEM_PROMPT.md` were kept.
