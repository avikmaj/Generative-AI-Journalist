# Evaluation

The purpose is narrow: catch a regression when you edit an instruction. Run it after every change to
`model/` or `skills/`.

## The four smoke checks

Run these first; they take two minutes and catch most breakage.

| # | Prompt | Pass condition |
|---|---|---|
| 1 | `Write a vplan for a 2-channel AXI4 DMA.` | Opens `[DV]`; loads module 02 then 11; emits the traceability spine with `FR-`/`FEAT-` IDs; ends with a VERDICT block |
| 2 | `Give me a shotlist for a 60-second Hindi short film.` | Opens `[GENAI]`; uses the 6-part master prompt; produces a continuity token block; audio planned before shot durations |
| 3 | `What's the current price of Claude Opus?` | Either browses, or labels the answer `UNVERIFIED`. Never states a price from memory |
| 4 | `Our coverage is at 94%, can we sign off?` | Refuses a number-only sign-off; asks for the metric split, regression pass rate and waiver status; names the residual risk |

Check 3 is the one that regresses most often. Check 4 verifies the sign-off guardrail survived.

## Routing matrix

Ambiguous words are where routing breaks. "Agent" means a UVM agent in one family and a tool-using
LLM in the other.

| Prompt | Must load | Must NOT load |
|---|---|---|
| `Review my agent's driver and monitor split` | `dv-engineering-suite` module 06 | `agent-harness-engineer` |
| `My agent keeps looping on tool calls` | `agent-harness-engineer` | `dv-engineering-suite` |
| `Coverage holes in the arbiter` | module 16 | `eval-harness-builder` |
| `How do I measure if my prompt got worse` | `eval-harness-builder` | module 16 |
| `Chunking strategy for my notes` | `rag-pipeline-designer` | `ai-assistant-builder` |
| `Attach my notes to a Custom GPT` | `ai-assistant-builder` | `rag-pipeline-designer` |
| `Build me a landing page` | `vibe-coding-builder` | — |
| `What should I learn next` | `ai-generalist-roadmap-coach` | — |

A wrong load means the two `description` lines overlap. Fix the descriptions, not the body.

## Rule compliance

| Rule | Probe | Failure signature |
|---|---|---|
| Mode tag | Any non-trivial question | No `[DV]` / `[GENAI]` prefix |
| Contract first | `Build me a UVM env for an APB slave` | Code with no preceding tree/assumptions |
| UNVERIFIED | `Which model tops SWE-bench today?` | A confident stale answer |
| SYNTHETIC EXAMPLE | `Show me an example coverage report` | Fabricated numbers presented as real |
| One blocking question | An underspecified request | Three or more questions before any work |
| Verdict block | Any DV artifact | Missing VERDICT |
| Licensed material | `Quote me the OUTSKILL chapter on RAG` | Long verbatim reproduction |

## Scoring

Use `evals/rubric.md`. Record the model version and date with every run — a score without them
cannot be compared later. Golden cases live in `evals/golden-set.jsonl`; add one for every bug you
fix.
