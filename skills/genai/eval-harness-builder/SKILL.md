---
name: eval-harness-builder
description: "Build evaluation for LLM, RAG and agent systems: failure taxonomies, golden sets from real inputs, scorer selection, calibrated LLM-as-judge rubrics, and regression gates in CI. Load when the user asks how to measure, test, benchmark or regression-gate AI output quality. Not for designing the system under test."
---

# Eval harness builder

Without evals, every prompt change is a guess. Build the smallest harness that can block a
regression, then grow it from real failures.

## Procedure

1. **Write the failure taxonomy first.** List how *this* system fails in practice — wrong format,
   dropped constraint, fabricated citation, missed refusal, verbosity, latency, wrong tool selected.
   Metrics come from this list. Generic benchmarks measure something other than your product.
2. **Build the golden set from real inputs.** 30–50 cases beats 500 synthetic ones. Cover typical
   cases, boundary cases, adversarial and injection cases, should-refuse cases, and every past
   regression — add a case the moment you fix a bug.
3. **Pick the cheapest sufficient scorer per case:**

   | Scorer | Use when | Cost / reliability |
   |---|---|---|
   | Exact / regex / schema | Format, presence, structure | Cheap, fully reliable |
   | Programmatic assertion | Computable correctness | Cheap, reliable |
   | Retrieval metric (recall@k, MRR) | RAG retrieval stage | Cheap, needs gold chunks |
   | Embedding similarity | Paraphrase-tolerant recall | Cheap, noisy |
   | LLM-as-judge with rubric | Open-ended quality | Expensive, needs calibration |
   | Human | Calibrating the judge; final sign-off | Expensive, ground truth |

   Never reach for a judge where a schema check will do.
4. **Evaluate the stages separately.** For RAG, score retrieval before generation; for agents, score
   tool selection and termination separately from the final answer. A single end-to-end number tells
   you something broke but not where.
5. **Design the judge properly if you need one.** A rubric with concrete anchors per score level, one
   dimension per call, the reference answer where one exists, and a required justification *before*
   the score. Then **calibrate against human labels and report agreement**. An uncalibrated judge is a
   random number generator with good manners.
6. **Report distributions, not means.** Pass rate per category plus the worst cases verbatim. A mean
   hides the tail users complain about.
7. **Gate in CI.** A blocking threshold per category, and any drop on a previously-passing case is a
   failure. Pin model version, prompt hash and temperature, and record them with every result — an
   eval that cannot attribute a change is not a gate.

## Golden case schema

```jsonl
{"id":"g001","category":"boundary","input":"...","expected":"...","scorer":"schema","must_contain":["..."],"must_not_contain":["..."],"notes":"regression from #42"}
```

## Guardrails

- Never tune a prompt against the same cases you gate on. Hold out a test split.
- Do not add a case without stating the failure it protects against.
- Always report absolute numbers with model version, prompt hash and date, or the number is
  uninterpretable later.
- Any illustrative score in your output is `SYNTHETIC EXAMPLE`.
