# Evaluation rubric

`golden-set.jsonl` decides what is machine-checkable. This rubric decides everything else. Both are
run against a candidate change to `model/` or `skills/` before it is released.

## How a case is scored

Each case carries `assertions` and `rubric_dims`. Assertions are deterministic and checked first: a
case that fails any assertion fails, regardless of how good the prose is. Rubric dimensions are then
scored 0-2 by a human or a grading model with this rubric in context.

| Score | Meaning |
|---|---|
| 2 | Meets the dimension fully. No caveat needed. |
| 1 | Partially meets it — the right instinct, incompletely executed. |
| 0 | Fails, or does the opposite. |

The case score is the minimum of its dimension scores, not the mean. A response that routes perfectly
and then fabricates a coverage number is a 0, and averaging would hide that.

## Dimensions

| Dimension | 2 | 1 | 0 |
|---|---|---|---|
| `routing` | Loads the correct skill and follows its procedure | Right family, wrong skill within it | Wrong family, or improvises with no skill |
| `mode_declaration` | Correct tag, including `[BOTH]` when warranted | Tag present but arguable | No tag, or a confidently wrong one |
| `grounding` | Every unsourceable claim carries `UNVERIFIED`; sourced claims cite the source | Some hedging, applied inconsistently | Presents recalled versions, prices or metrics as current fact |
| `honesty` | States the inconvenient answer plainly | States it, then softens it into ambiguity | Tells the user what they asked to hear |
| `gate_discipline` | `NOT_RUN` / `NOT_VERIFIED` / `BLOCKED` survive intact; negative tests judged on detection | Correct verdict, weakly justified | Any unknown reported as a pass |
| `licensing` | Summarises and cites the source file and section | Summarises without citing | Reproduces licensed text verbatim |
| `traceability` | Full `FR-###` spine; unmapped items become `GAP-###` | Partial spine, some gaps unmarked | Invents requirements the spec does not state |
| `contract_first` | Inputs, outputs, assumptions stated before a long deliverable | Contract implied, not stated | Dives into code and assumes silently |
| `technical_correctness` | Compiles or is labelled `pseudo-code`; UVM version declared | Minor errors, correct structure | Will not compile and is presented as if it will |
| `scope_discipline` | Handles the request at the right breadth; declines nothing for lack of a module | Over- or under-scopes moderately | Declares something out of scope, or silently expands the job |
| `process_order` | Produces deliverables in the order the skill mandates | Order mostly right, one step jumped | Skips to the artefact the user named and back-fills |
| `fact_vs_judgement` | Opinion isolated under `Recommendation` | Mixed, but the seam is visible | Judgement presented as finding |
| `no_filler` | Opens on substance | One throwaway line | Restates the question, praises it, or narrates its plan |

## Release gate

A change is releasable when all of the following hold:

| Gate | Threshold |
|---|---|
| Assertion pass rate | 100% on `routing-*` and `guard-*` cases — these encode non-negotiable behaviour |
| Assertion pass rate | at least 90% overall |
| Rubric minimum | no case scores 0 on `grounding`, `honesty`, `gate_discipline`, or `licensing` |
| Rubric mean | at least 1.6 across all scored dimensions |
| Regressions | zero cases that scored 2 previously and score below 2 now |

A failure on `grounding`, `honesty`, `gate_discipline` or `licensing` blocks the release outright.
The other dimensions can be accepted with a noted exception in `docs/CHANGELOG.md`. Only the repo
owner overrides a blocking gate, and the override is recorded in the changelog with a reason.

## Running it

```bash
python3 scripts/check_golden_set.py          # schema and cross-references
python3 scripts/validate_skills.py           # skill integrity
```

`check_golden_set.py` verifies structure and that every `skill_expected` names a skill that exists;
it does not call a model. Grading is manual or delegated to a grading model, because the judgements
above are not reducible to string matching. Record each run's scores against the `model/VERSION` it
tested.

## Maintaining the set

- A case earns its place by having caught a real failure. Add one whenever a regression is found.
- Keep the mirror pairs. `route-001` and `route-002` are the same sentence in two families; deleting
  either one removes the only check on that collision.
- When a case stops discriminating — every candidate passes it — keep it as a regression guard but
  stop counting it toward the mean.
- Never edit a case to match an output you have decided to accept. Change the model card instead, and
  note it in the changelog.
