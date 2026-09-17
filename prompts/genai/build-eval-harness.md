# Build an eval harness

Expected skill: `eval-harness-builder`. Expected mode: `[GENAI]`.

```text
Build an evaluation harness for this system.

System under test: <WHAT IT DOES>
What "good" means here: <IN THE USER'S OWN WORDS>
Current quality signal: <MANUAL SPOT CHECKS / NOTHING / EXISTING TESTS>
Budget: <RUNS PER DAY OR COST CEILING>

Return:
1. A golden set spec: how many cases, how they are sampled, and what makes a case worth keeping.
2. Ten concrete starter cases in JSONL, each with the assertion that decides pass or fail.
3. A rubric for anything not machine-checkable, with the scoring scale anchored by examples.
4. The regression gate: which metric blocks a release, at what threshold, and who can override.

Prefer deterministic assertions over model-graded scores wherever the output allows it. State the
inter-rater ambiguity for any rubric dimension you propose.
```

## Why it is shaped this way

Harnesses fail by scoring what is easy rather than what matters. Forcing the release gate to be named
up front makes the harness consequential instead of decorative.
