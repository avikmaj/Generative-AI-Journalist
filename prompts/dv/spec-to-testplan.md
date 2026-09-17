# Spec to verification plan

Expected skill: `dv-engineering-suite`. Expected mode: `[DV]`.

```text
Convert the attached specification into a verification plan.

Spec: <ATTACH OR PASTE SPEC>
DUT: <BLOCK NAME>
Scope: <FEATURES IN SCOPE>  Out of scope: <EXPLICIT EXCLUSIONS>

Produce, in this order:
1. A numbered feature list, FR-001 onward, each traceable to a spec section number.
2. A verification-condition table: FR-### -> FEAT-### -> VC-### -> proposed SEQ-### and COV-###/SVA-###.
3. Any requirement the spec leaves ambiguous, as a GAP-### row with the exact question to ask.

Rules: do not invent a requirement the spec does not state. If a field width, reset value or timing
number is absent, raise it as GAP-### rather than assuming. Mark anything you inferred UNVERIFIED.
```

## Why it is shaped this way

The traceability spine is the deliverable, not prose. Forcing GAP-### rows makes spec ambiguity
visible instead of quietly absorbed into an assumption that later reads as verified.
