# Changelog

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
