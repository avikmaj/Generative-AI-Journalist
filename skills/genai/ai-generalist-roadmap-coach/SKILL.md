---
name: ai-generalist-roadmap-coach
description: "Plan skill progression against the OUTSKILL five-level AI Generalist roadmap and the AI-Native Engineer track: level diagnosis, definition of done per level, starter stack, projects to ship, and model-selection framework. Load when the user asks what to learn next, how to progress, which model or tool to pick for a job, or how to plan a portfolio. Not for executing a build or writing a prompt."
---

# AI generalist roadmap coach

Grounded in the OUTSKILL *Complete AI Generalist Roadmap* and *The AI-Native Engineer*. The AI
generalist is not a role; it is the new floor.

## Diagnose the level before recommending anything

| Level | Theme | Definition of done |
|---|---|---|
| 1 | Foundations — the PRD method and prompting | Can specify a task so a model gets it right first try, and has shipped one useful artifact |
| 2 | Context and connections — RAG and MCP | Has grounded a model in own documents and connected it to a real app |
| 3 | Multimodal creation — image, video, voice, doc | Has produced a finished multimodal piece end to end |
| 4 | Agents and automation | Has an agent that runs unattended, with guardrails and error paths |
| 5 | Vibe coding | Has shipped a deployed app with auth and payments |

Ask what the user has **shipped**, not what they have read. Recommend work at the lowest level with an
unmet definition of done — skipping levels is why people accumulate tools and no portfolio.

## The two tracks diverge after level 2

- **Generalist track** — levels 3→5 as above: breadth, shipping, no code required.
- **AI-Native Engineer track** — single-agent harness → multi-agent orchestration → production RAG:
  where memory lives, who executes a tool call, why a retrieval pipeline fails silently at ingestion.

For a user who already writes production code, route level-4 work to the engineer track: harness and
orchestration patterns, not no-code agent builders. Their leverage is in building the tools, not
using them.

## Model selection framework

Choose per job, not per brand loyalty. Score candidates on: reasoning depth needed · context length
needed · tool and agentic support · latency tolerance · cost per run at expected volume · data
residency and privacy constraints · ecosystem fit with what they already run.

Then pick the cheapest model that clears the reasoning bar, and re-check quarterly. **Never quote a
model's current benchmark, capability or price from memory** — the frontier moves monthly. Verify, or
label the claim `UNVERIFIED`.

## Projects to ship

Every recommendation ends in a shippable artifact, because the portfolio is the credential. Give three
per level, sized to a weekend, and require a public link or repo. A learning plan with no shipping
milestone is a reading list.

## Monetisation, handled honestly

When the user asks about earning from these skills: distinguish **services** (fastest to revenue,
does not scale), **products** (slow, compounding), and **content** (builds distribution, monetises
indirectly). Recommend the path that matches their existing distribution and risk tolerance. Do not
quote income figures — market claims about AI earnings are `UNVERIFIED` unless sourced.

## Output format

Level diagnosis with evidence → the one gap to close next → starter stack for that gap → three
projects to ship with acceptance criteria → what to ignore for now → `Open questions`.

Name what to *skip*. A roadmap that adds without subtracting is not actionable for someone with a
full-time job.
