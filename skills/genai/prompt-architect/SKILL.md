---
name: prompt-architect
description: "Design, refactor and harden prompts using the OUTSKILL 6-part formula, CoStar, ACR and chain-of-thought patterns, with explicit output contracts and context-window hygiene. Load when the user asks to write, review, improve or debug a prompt or system prompt. Not for retrieval pipelines or evaluating output at scale."
---

# Prompt architect

Grounded in OUTSKILL Book One, *The AI Generalist Mindset*. A prompt is an interface specification;
treat vagueness as a defect.

## The 6-part formula — the default skeleton

| Part | Supplies |
|---|---|
| Role | Who the model should be |
| Context | The facts it cannot know |
| Task | The one thing to do |
| Format | The exact shape of the answer |
| Constraints | Length, tone, what to avoid |
| Example | One sample, when shape matters |

Every prompt you write or review must have all six, or a stated reason one is absent. A missing
`Format` is the most common defect; a missing `Context` is the most expensive.

## Procedure

1. **Name the job precisely.** One prompt, one task. Two verbs with different output shapes means two
   prompts, chained.
2. **Write the output contract before the prose**: shape, field names, ordering, length bounds, and
   what to emit when the input is unusable. Most failures are unspecified edge behaviour, not weak
   wording.
3. **Pick the framework that matches the job**, rather than defaulting to one:

   | Framework | Use when |
   |---|---|
   | 6-part formula | Any single-turn generation task |
   | CoStar (Context, Objective, Steps, Tools, Reflection) | The task has a procedure and tool access |
   | Chain-of-thought | Reasoning must be inspected before the verdict |
   | Socratic | Requirements are unclear — make the model interrogate the user first |
   | ACR (Ask, Check, Recommend) | Advisory output where a wrong confident answer is costly |

4. **Enumerate failure modes before drafting.** List what a plausible-but-wrong answer looks like:
   fabricated citation, dropped constraint, hedged non-answer, wrong format, missed refusal. Add one
   targeted instruction per mode. Skipping this yields a happy-path-only prompt.
5. **Budget the context window.** Fill it with just the right information and no more. Rising input
   length quietly degrades quality — context rot, the "lost in the middle" effect. When a prompt grows
   past a screen, move stable material into reference files or a Project knowledge base rather than
   pasting it every turn.
6. **Choose examples deliberately.** Two well-chosen shots beat six similar ones. Include one boundary
   case and one refusal case; examples teach format far better than prose.
7. **Order for attention**: role → contract → rules → examples → input. Repeat the single
   most-violated constraint at the end as well as the start.
8. **Test against paraphrases.** Two rewordings that should trigger the same behaviour, and one
   adjacent request that should not. Report what broke.

## Advanced techniques — when each earns its cost

`zero-shot` for well-known tasks · `few-shot` when format is idiosyncratic · `chain-of-thought` when
the reasoning must be auditable · `self-consistency` when a single sample is unreliable and you can
afford N runs · `tree-of-thoughts` for search over branching plans · `ReAct` when the model must
interleave reasoning with tool calls. Do not stack these; each adds tokens and failure surface.

## Anti-patterns to remove on sight

| Pattern | Why it fails | Replace with |
|---|---|---|
| "Be detailed and thorough" | Unmeasurable | A length bound and a required-section list |
| "Think step by step" bolted on | Redundant on reasoning models | A named decomposition, or nothing |
| "Do not hallucinate" | Not actionable | "Cite a source per claim; write UNVERIFIED otherwise" |
| Politeness padding | Costs tokens, changes nothing | Delete |
| Stacked negations | Models track positives better | State the desired behaviour |
| Wall-of-text system prompt | Instructions compete | Markdown headings: `## Role`, `## Rules`, `## Steps` |
| Everything in one mega-prompt | Context rot | Chain, or move detail to knowledge files |

## Output when reviewing a prompt

Missing formula parts → failure modes found → line-referenced defect list → rewritten prompt → what
to test. A good prompt is cheaper than the round-trip it prevents.
