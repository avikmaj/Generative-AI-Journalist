---
name: ai-workflow-designer
description: "Turn one-off prompts into repeatable chained workflows and choose the integration layer — connector, MCP, API or RAG — so the model can act across apps. Covers the DRA deck pattern, ACR, and disciplined AI data analysis. Load when the user asks about AI workflows, chaining prompts, connectors, or analysing a data file with AI. Not for n8n canvas builds or agent harness code."
---

# AI workflow designer

Grounded in OUTSKILL Book Three. A prompt is one turn; a workflow is a repeatable chain where each
step's output feeds the next — so the same quality comes out every time, not just when you get the
wording right.

## Procedure

1. **Find the repeat.** If the user runs the task once, write a prompt. Build a workflow only when the
   task recurs or the output quality must be consistent across runs.
2. **Break the job into steps, give each step a role, then chain.** One role per step. A step that
   does two jobs is where quality collapses.
3. **Define the handoff between steps** explicitly: what artifact step N produces, in what shape, that
   step N+1 consumes. Unspecified handoffs are the main failure point in chained workflows.
4. **Choose the integration layer deliberately:**

   | Layer | What it is | Choose when |
   |---|---|---|
   | Connector | Model acts inside an app — fast, no code | The app is supported and you need action now |
   | MCP | The open standard behind connectors | You need a reusable, portable tool surface |
   | API | Full control, needs code | Custom logic, volume, or an unsupported app |
   | RAG | Grounds answers in your documents | The answer lives in your files, not in an app |

   These are not a maturity ladder — pick the cheapest layer that does the job.
5. **Add a verification step.** Every workflow that produces an external artifact ends with a check
   step against the source, not with the generation step.

## The ACR pattern

**Ask** — clarify before acting. **Check** — verify against the source. **Recommend** — one clear next
step. Use it for any advisory step where a confident wrong answer is costly.

## The DRA deck workflow

Three sequential passes over one deck, each with its own prompt and role:

1. **Designer** — structure and visual flow: the narrative spine and slide sequence.
2. **Researcher** — gather and verify the facts that each slide asserts.
3. **Analyst** — turn the data into the story, and cut what does not serve it.

Run them in sequence, never merged into one prompt. The same three-pass shape generalises to reports,
proposals and documentation.

## AI data analysis, done properly

1. Upload the file and **make the model restate the columns first**, including types and row count.
   If its restatement is wrong, every downstream number is wrong.
2. **Ask ordered questions, not "what's interesting".** Open-ended requests produce plausible
   summaries of nothing.
3. **Force a "so what" after every number.** A figure without an implication is not analysis.
4. Ask it to state the assumption behind any aggregate, and to name rows it excluded.
5. Never accept a computed figure you cannot see the calculation for. Require the code or the steps.

## Output format

Trigger → step table (`#`, role, input, output artifact, tool) → integration layer choice with
rationale → verification step → failure handling → `Open questions`.
