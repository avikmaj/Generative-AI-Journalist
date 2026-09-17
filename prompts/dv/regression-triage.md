# Regression triage

Expected skill: `vip-factory` for release gating, `dv-engineering-suite` for root cause.
Expected mode: `[DV]`.

```text
Triage this regression.

Regression log / summary: <ATTACH>
Seeds run: <N>  Passed: <N>  Failed: <N>  Not run: <N>
Build under test: <COMMIT OR TAG>

Return:
1. A failure-signature table: signature, count, affected tests, first failing seed, suspected owner
   (DUT / TB / test / environment).
2. Whether the run meets the PASS policy. Apply it literally — NOT_RUN is not a pass, and a negative
   test passes only if the violation was actually detected.
3. For each distinct signature, the next diagnostic step that would discriminate between causes.
4. A BUG-### draft for any signature you believe is a real DUT bug.

Do not aggregate distinct signatures into one bug to make the count look smaller. State the verdict
even if it blocks the release.
```

## Why it is shaped this way

Triage pressure is toward a clean-looking summary. Naming the not-run count as a separate input and
forbidding signature merging keeps the release verdict honest.
