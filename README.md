# Generative-AI-Journalist

A portable **generative-AI model definition and skill library** that drives the same behaviour
across **Claude Projects**, **ChatGPT Custom GPTs** and **Grok projects**, from one source of truth
in this repo.

## Skill families

| Family | Path | Skills | Purpose |
|---|---|---|---|
| `dv` | `skills/dv/` | 2 | Semiconductor design verification — UVM methodology and evidence-gated VIP execution |
| `genai` | `skills/genai/` | 10 | Generative-AI engineering — prompts, vibe coding, workflows, assistants, n8n, RAG, agents, evals |
| `business` | `skills/business/` | 1 | Business management — leadership, strategy, projects, sales, marketing, finance, people, risk |
| `film` | `skills/film/` | 1 | AI film production — story to screenplay to shot list to generation prompts to QC |

Every family is independent. Each skill's `description` ends with an explicit negative guard clause
so families never collide on shared words like *agent*, *coverage*, *sequence* or *pipeline*.

## Why this layout

Claude, ChatGPT and Grok expose different surfaces — project instructions plus Agent Skills, versus
a single system prompt plus knowledge files and actions, versus project instructions with a context
budget. Rather than maintaining three divergent prompt sets, the canonical definitions live in
`model/` and `skills/`, and the build scripts render platform-specific artifacts into `dist/`.

```
model/ + skills/  ──►  build_claude_bundle.py    ──►  dist/claude/
                  ──►  build_chatgpt_bundle.py   ──►  dist/chatgpt/
                  ──►  build_grok_bundle.py      ──►  dist/grok/
```

`dist/` is generated and git-ignored. Never edit it by hand.

## Repository map

```
model/                    Canonical model card: identity, operating rules, refusal policy
platforms/claude/         Claude Project instructions + CLAUDE.md
platforms/chatgpt/        Custom GPT system prompt, starters, knowledge manifest, Actions schema
platforms/grok/           Grok project instructions + VIP factory team rules
skills/dv/                Design-verification family
skills/genai/             Generative-AI engineering family
skills/business/          Business management family
skills/film/              AI film production family
knowledge/dv/             DV Engineering Bible, agentic DV architecture
knowledge/outskill/       Drop-zone for the OUTSKILL course corpus (git-ignored, see its README)
knowledge/business/       Business Bible drop-zone + 59-book catalogue (bibles git-ignored)
knowledge/film/           AI Film Production Bible volumes 1-4
prompts/                  Reusable task prompts, grouped by family
evals/                    Golden question set + scoring rubric
scripts/                  Ingest, build and validate tooling
docs/                     Setup, architecture and authoring guides
```

## Quick start

```bash
git clone https://github.com/avikmaj/Generative-AI-Journalist.git
cd Generative-AI-Journalist
python -m pip install -r requirements.txt

# Validate every skill package (runs in CI too)
python3 scripts/validate_skills.py
```

Then follow [docs/02-setup-claude.md](docs/02-setup-claude.md),
[docs/03-setup-chatgpt.md](docs/03-setup-chatgpt.md) and
[docs/04-setup-grok.md](docs/04-setup-grok.md).
For a single copy-paste checklist covering all three platforms, project names, objectives, exact
upload lists and test prompts, see [docs/08-project-setup.md](docs/08-project-setup.md).
To work through the uploads step by step, use
[docs/09-upload-checklist.md](docs/09-upload-checklist.md).
To read corpora straight from this repo instead of uploading copies, see
[docs/10-github-direct-access.md](docs/10-github-direct-access.md).

## Skill index

### Design verification — `skills/dv/`

| Skill | Shape | Use for |
|---|---|---|
| `dv-engineering-suite` | 1 hub + 23 reference modules | Methodology: vplan, UVM architecture, agents, sequences, scoreboard, RAL, protocols (AMBA, high-speed, embedded, NoC), formal and SVA, coverage, debug, agentic DV, regression automation, signoff |
| `vip-factory` | 1 hub + 9 references + skeleton, CI and runner assets | Execution: build, compile, simulate, regress L0–L5, gates 0–11, PASS authority policy, coverage and assertion gates, signoff artifacts |

The split is deliberate. `dv-engineering-suite` teaches technique; `vip-factory` runs the
organization and owns the rule that **PASS requires simulator evidence and is never inferred**.

### Generative AI — `skills/genai/`

`prompt-architect` · `vibe-coding-builder` · `ai-workflow-designer` · `ai-assistant-builder` ·
`n8n-agent-builder` · `agent-harness-engineer` · `rag-pipeline-designer` ·
`visual-storytelling-director` · `eval-harness-builder` · `ai-generalist-roadmap-coach`

Ten independent skills, because these are genuinely separate jobs with different inputs and outputs.

### Business management — `skills/business/`

`business-management` — one hub with a domain router over 10 references (leadership and management,
strategy, projects, sales, marketing, finance, people, technology, advisory, templates) plus
fill-in scaffolds for a risk register, one-page strategy, OKRs and a decision brief.

### AI film production — `skills/film/`

`ai-movie-studio` — one hub with a deliverable router over 60 modules across core craft, audio, VFX,
genre prompt libraries, model adapters, asset bibles, quality control and worked examples.

## Architecture note

Two packaging patterns are used deliberately, and the choice is explained in
[docs/01-architecture.md](docs/01-architecture.md):

- **One hub plus reference modules** when the domain shares invariants and needs a single router —
  `dv-engineering-suite`, `vip-factory`, `business-management`, `ai-movie-studio`.
- **Many independent skills** when the tasks are genuinely separate jobs — the `genai` family.

## Licensed material

Some source corpora are third-party licensed and are **never committed**:
`knowledge/outskill/raw/`, `knowledge/outskill/index.jsonl`, `knowledge/business/raw/` and the
Business Management Bible compilations. Only the structure, catalogues and original synthesis are
tracked. CI fails the build if any of these become tracked.

## Licence

MIT — see [LICENSE](LICENSE). The MIT licence covers this repository's own content, not the
third-party corpora referenced above.
