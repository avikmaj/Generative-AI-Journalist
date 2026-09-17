# Source map — fetch from GitHub instead of uploading

This repository is **private**. The raw URLs below are therefore *addresses, not public links* — an
unauthenticated fetch returns 404, which is correct behaviour.

They work in exactly two ways:

1. Through Claude's GitHub integration, which reads the repo as your authenticated GitHub account.
2. Through an authenticated call to the GitHub contents API with a token that has `repo` scope.

If the repository is ever made public, these become plain fetchable links and any platform with web
access can use them directly. Nothing in this repository is licensed third-party material — that is all
git-ignored — so making it public is feasible, but it is a deliberate choice, not the current state.

Repository: https://github.com/avikmaj/Generative-AI-Journalist (private)

## What must NOT be fetched on demand

Instructions and skill bodies. They have to be present on every turn, and a failed fetch is
indistinguishable from a skill that says nothing — the model improvises and you get a confident answer
with no procedure behind it. Keep those uploaded or pasted. See
[docs/10-github-direct-access.md](../docs/10-github-direct-access.md).

Fetch-on-demand is appropriate for the large reference corpora below, where a failure is graceful: the
model can say it could not read the file.

## How to use this file

When you need a corpus fact, read the file at the path below, then cite what you actually read. If you
cannot reach it, say so plainly — never fall back to recall and present it as sourced. While the
repository is private, an unauthenticated fetch WILL fail; that is expected and is not evidence the
content is missing. Cite as
`DV_Bible §<section>`, `FilmBible/<volume> §<section>`, `OUTSKILL/<file> §<section>`.

## Reference corpora — safe to fetch on demand

| File | Size | Raw URL |
|---|---|---|
| `knowledge/business/LIBRARY.md` | 2 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/business/LIBRARY.md |
| `knowledge/business/README.md` | 2 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/business/README.md |
| `knowledge/dv/AI_DV_Master_Engineer_v3_1.md` | 71 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/dv/AI_DV_Master_Engineer_v3_1.md |
| `knowledge/dv/DV_Bible_Index.md` | 6 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/dv/DV_Bible_Index.md |
| `knowledge/dv/DV_Engineering_Bible_Vol1.md` | 401 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/dv/DV_Engineering_Bible_Vol1.md |
| `knowledge/dv/README.md` | 1 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/dv/README.md |
| `knowledge/dv/agentic_ai_dv_architecture.md` | 18 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/dv/agentic_ai_dv_architecture.md |
| `knowledge/film/AI_Film_Production_Bible_v2_Vol1.md` | 284 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/film/AI_Film_Production_Bible_v2_Vol1.md |
| `knowledge/film/AI_Film_Production_Bible_v2_Vol2.md` | 71 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/film/AI_Film_Production_Bible_v2_Vol2.md |
| `knowledge/film/AI_Film_Production_Bible_v2_Vol3.md` | 47 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/film/AI_Film_Production_Bible_v2_Vol3.md |
| `knowledge/film/AI_Film_Production_Bible_v2_Vol4.md` | 44 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/film/AI_Film_Production_Bible_v2_Vol4.md |
| `knowledge/film/README.md` | 1 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/film/README.md |
| `knowledge/outskill/CURRICULUM.md` | 6 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/outskill/CURRICULUM.md |
| `knowledge/outskill/README.md` | 2 KB | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/knowledge/outskill/README.md |

## Canonical definition

| File | Raw URL |
|---|---|
| `model/MODEL_CARD.md` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/model/MODEL_CARD.md |
| `model/VERSION` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/model/VERSION |

## Skill bodies — upload these, do not fetch them

Listed for reference and for verifying an upload matches the repository. A skill you fetch
instead of installing is a skill that silently vanishes when the fetch fails.

| Skill | Raw URL |
|---|---|
| `business-management` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/business/business-management/SKILL.md |
| `dv-engineering-suite` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/dv/dv-engineering-suite/SKILL.md |
| `vip-factory` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/dv/vip-factory/SKILL.md |
| `ai-movie-studio` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/film/ai-movie-studio/SKILL.md |
| `agent-harness-engineer` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/agent-harness-engineer/SKILL.md |
| `ai-assistant-builder` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/ai-assistant-builder/SKILL.md |
| `ai-generalist-roadmap-coach` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/ai-generalist-roadmap-coach/SKILL.md |
| `ai-workflow-designer` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/ai-workflow-designer/SKILL.md |
| `eval-harness-builder` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/eval-harness-builder/SKILL.md |
| `n8n-agent-builder` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/n8n-agent-builder/SKILL.md |
| `prompt-architect` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/prompt-architect/SKILL.md |
| `rag-pipeline-designer` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/rag-pipeline-designer/SKILL.md |
| `vibe-coding-builder` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/vibe-coding-builder/SKILL.md |
| `visual-storytelling-director` | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/skills/genai/visual-storytelling-director/SKILL.md |

## Prompts and evaluation

| File | Raw URL |
|---|---|
| Prompt library index | https://github.com/avikmaj/Generative-AI-Journalist/blob/main/prompts/README.md |
| Golden set | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/evals/golden-set.jsonl |
| Rubric | https://raw.githubusercontent.com/avikmaj/Generative-AI-Journalist/main/evals/rubric.md |

## Never fetch these — they do not exist publicly, by design

The OUTSKILL course PDFs (`knowledge/outskill/raw/`), the extracted corpus index
(`knowledge/outskill/index.jsonl`), the purchased business e-books (`knowledge/business/raw/`)
and the Business Management Bible compilations are git-ignored licensed material. A 404 on any
of those paths is correct behaviour, not a broken link.
