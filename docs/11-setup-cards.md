# Setup cards — Claude, ChatGPT, Grok

Use one card per platform. This version is sized for **ChatGPT Plus** and **Claude Max**. The GitHub
connector is already connected, so large reference corpora stay in the private repository. Only files
that must be available on every turn are uploaded.

## Limits already handled

| Platform | Instruction file | Characters | Uploads required | Guardrail |
|---|---|---:|---:|---|
| Claude Max | `01-CLAUDE/project-instructions.md` | under 2,100 | 14 skill zips, 0 markdown | Project files are unlimited; 30 MB each |
| ChatGPT Plus | `02-CHATGPT/system-prompt.md` | under 4,000 | 5 markdown | Below OpenAI's 20-file, 512 MB/file GPT knowledge limit |
| Grok | `03-GROK/project-instructions.md` | under 4,000 | 5 markdown | Below the conservative six-at-a-time desktop envelope |

The builders fail if ChatGPT or Grok instructions exceed 4,000 characters or if either bundle exceeds
five upload files. Do not copy instructions from `platforms/` in GitHub: those are pre-build sources.
Always paste the built instruction file from the download package.

Repository:

```text
https://github.com/avikmaj/Generative-AI-Journalist
```

The repository is private. Select it through the authenticated GitHub connector; raw GitHub URLs
return 404 without authentication.

---

# Claude Project

## Project Name

```text
Generative AI Journalist
```

## Objective

```text
Act as my senior technical collaborator across semiconductor design verification, generative-AI
systems engineering, business management, and AI film production. Select and follow the matching
installed skill instead of improvising. Declare the active mode, cite repository material actually
read, and never report unrun or unverified work as passing.
```

## Project Instructions

1. Open `01-CLAUDE/project-instructions.md`.
2. Copy only the text after the `---` separator.
3. Paste it into Project settings → Custom instructions.
4. Confirm the field starts with `You are Generative AI Journalist`.

The pasted block is under 2,100 characters.

## All files pointed to GitHub repo

Project knowledge → **+** → **GitHub** → select the repository, then these files:

```text
model/MODEL_CARD.md
knowledge/dv/DV_Engineering_Bible_Vol1.md
knowledge/dv/AI_DV_Master_Engineer_v3_1.md
knowledge/dv/agentic_ai_dv_architecture.md
knowledge/outskill/CURRICULUM.md
```

Optional for film work:

```text
knowledge/film/AI_Film_Production_Bible_v2_Vol1.md
```

Do not select the whole repository. After each future `git push`, use Claude's **Sync now** action.

## Markdown files to upload in project context

None.

## Other required uploads

Upload all 14 zips from `01-CLAUDE/skill-zips/` as Agent Skills:

```text
dv-engineering-suite.zip
vip-factory.zip
prompt-architect.zip
vibe-coding-builder.zip
ai-workflow-designer.zip
ai-assistant-builder.zip
n8n-agent-builder.zip
agent-harness-engineer.zip
rag-pipeline-designer.zip
visual-storytelling-director.zip
eval-harness-builder.zip
ai-generalist-roadmap-coach.zip
business-management.zip
ai-movie-studio.zip
```

Do not upload `CLAUDE.md`; it is for a local Claude Code checkout.

## Example prompts to test the whole project

Run each in a new thread:

```text
My agent isn't seeing transactions on the analysis port. Where do I look first?
```

Expected: `[DV]`, UVM monitor and `connect_phase`.

```text
My agent loops forever calling the same tool. How do I fix the termination condition?
```

Expected: `[GENAI]`, termination condition, no UVM vocabulary.

```text
Regression: 180 seeds, 172 passed, 0 failed, 8 did not run because the grid was full.
Can I mark this PASS and release?
```

Expected: refusal; `NOT_RUN` is not PASS.

```text
Open knowledge/dv/DV_Engineering_Bible_Vol1.md from the connected repo and quote the section
that defines the traceability spine. Cite the section.
```

Expected: a real repository citation containing `FR-###` through `AGT-###`.

## Skill-specific test prompts

Use the shared skill table at the end of this document.

---

# ChatGPT Custom GPT

## Project Name

```text
Generative AI Journalist
```

## Objective

```text
Act as my senior technical collaborator across semiconductor design verification, generative-AI
systems engineering, business management, and AI film production. Route every task to the matching
uploaded skill, cite repository material actually read, and never report unrun or unverified work
as passing.
```

## Project Instructions

1. Open `02-CHATGPT/system-prompt.md`.
2. Copy only the text after the first `---` separator.
3. Paste it into Configure → Instructions.
4. Confirm `## Skill router` and all 14 skill names are present at the bottom.

The built block is under 4,000 characters. Never paste
`platforms/chatgpt/system-prompt.md` directly from GitHub; that source does not contain the generated
router.

## All files pointed to GitHub repo

Use the connected repository for bulky corpora:

```text
model/MODEL_CARD.md
knowledge/dv/DV_Engineering_Bible_Vol1.md
knowledge/dv/AI_DV_Master_Engineer_v3_1.md
knowledge/dv/agentic_ai_dv_architecture.md
knowledge/film/AI_Film_Production_Bible_v2_Vol1.md
knowledge/outskill/CURRICULUM.md
```

These do not need separate knowledge uploads.

## Markdown files to upload in project context

Upload exactly these 5 files from `02-CHATGPT/upload-these-5/`:

```text
FAMILY_DV.md
FAMILY_GENAI.md
FAMILY_BUSINESS.md
FAMILY_FILM.md
CONTROL.md
```

The four family files contain all 14 flattened skills. `CONTROL.md` contains the model policy and
reusable prompts. This replaces the old 17-file ChatGPT set.

## Example prompts to test the whole project

Run the four Claude whole-project prompts above. Then ask:

```text
Name the exact uploaded file and # Skill heading you used for that answer.
```

Expected: one `FAMILY_*.md` file and a real `# Skill:` heading.

## Skill-specific test prompts

Use the shared skill table at the end.

---

# Grok Project

## Project Name

```text
Generative AI Journalist
```

## Objective

```text
Act as my senior technical collaborator across semiconductor design verification, generative-AI
systems engineering, business management, and AI film production. Route every task to the matching
uploaded skill, cite repository material actually read, and never report unrun or unverified work
as passing.
```

## Project Instructions

1. Open `03-GROK/project-instructions.md`.
2. Copy only the text after the first `---` separator.
3. Paste it into the project instructions field.
4. Confirm `## Skill router` and all 14 skill names are present at the bottom.

The built block is under 4,000 characters.

## All files pointed to GitHub repo

Use the connected repository for bulky corpora:

```text
model/MODEL_CARD.md
knowledge/dv/DV_Engineering_Bible_Vol1.md
knowledge/dv/AI_DV_Master_Engineer_v3_1.md
knowledge/dv/agentic_ai_dv_architecture.md
knowledge/film/AI_Film_Production_Bible_v2_Vol1.md
knowledge/outskill/CURRICULUM.md
```

If Grok cannot open a private-repo path through the connector, report the access failure; do not
substitute a web-search result.

## Markdown files to upload in project context

Upload exactly these 5 files from `03-GROK/upload-these-5/`:

```text
FAMILY_DV.md
FAMILY_GENAI.md
FAMILY_BUSINESS.md
FAMILY_FILM.md
CONTROL.md
```

`CONTROL.md` also contains the governing VIP team rules, so there is no separate seventh upload.

## Example prompts to test the whole project

Run the four Claude whole-project prompts above. Pay particular attention to:

```text
What is the current UVM version, and what is the context window and price of the newest Claude model?
```

Expected: current claims are sourced from a live source or labelled `UNVERIFIED`.

## Skill-specific test prompts

Use the shared skill table below.

---

# Shared skill-specific test prompts

| Skill | Prompt | Expected route |
|---|---|---|
| `dv-engineering-suite` | `Create a UVM monitor and coverage plan for this interface.` | `[DV]`, DV engineering procedure |
| `vip-factory` | `Kick off a new I3C target VIP at L2.` | `[DV]`, Gate 0, `FR-###`, `NOT_VERIFIED` |
| `prompt-architect` | `Harden this system prompt so it stops answering outside scope.` | `[GENAI]`, prompt failure analysis |
| `vibe-coding-builder` | `Direct the first iteration of a regression dashboard app.` | `[GENAI]`, stack and iteration loop |
| `ai-workflow-designer` | `Design a nightly regression-to-Slack workflow.` | `[GENAI]`, trigger, steps, error path |
| `ai-assistant-builder` | `Package my DV knowledge into a reusable assistant.` | `[GENAI]`, instructions/knowledge split |
| `n8n-agent-builder` | `Build that workflow specifically in n8n.` | `[GENAI]`, n8n nodes and credentials |
| `agent-harness-engineer` | `My tool-calling agent loops forever.` | `[GENAI]`, termination guard |
| `rag-pipeline-designer` | `Ground answers in 400 pages of specifications.` | `[GENAI]`, parsing, chunking, retrieval |
| `visual-storytelling-director` | `Write one cleanroom hero-image prompt.` | `[GENAI]`, single-shot direction |
| `eval-harness-builder` | `Measure whether my prompt change improved quality.` | `[GENAI]`, golden set and rubric |
| `ai-generalist-roadmap-coach` | `Sequence the AI skills I should learn next.` | `[GENAI]`, staged roadmap |
| `business-management` | `Build the case for two verification headcount.` | `[BIZ]`, business assumptions |
| `ai-movie-studio` | `Plan a six-episode Hindi animated series.` | `[FILM]`, end-to-end production |

# Final sign-off

Run this on all three:

```text
Kick off a new I3C target VIP at L2.
```

All three must return `[DV]`, Gate 0, spec-derived `FR-###` rows, and
`STATUS: NOT_VERIFIED`. None may call I3C unsupported. Record `model/VERSION`; currently `1.1.1`.

# Limit sources

- Claude project files are unlimited subject to context capacity, with a 30 MB per-file limit:
  https://support.claude.com/en/articles/8241126-upload-files-to-claude
- OpenAI permits up to 20 knowledge files per GPT, each up to 512 MB:
  https://help.openai.com/en/articles/8554397-creating-and-editing-gpts
- xAI documents six desktop attachments at a time for its desktop composer:
  https://docs.x.ai/grok-bot/files-and-results

The 4,000-character instruction ceiling is a conservative repository policy, not a claim that all
three products publish the same limit. The builders enforce it to absorb platform and plan changes.
