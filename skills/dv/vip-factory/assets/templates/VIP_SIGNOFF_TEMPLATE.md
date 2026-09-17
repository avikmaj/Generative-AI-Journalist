# VIP SIGNOFF DOCUMENT
## AVIK VIP Factory · Fill in for each VIP release

---

## Header

```
VIP:              <vip_name>
Protocol:         <protocol + version>
Version:          <vip_version>
Git Tag:          <tag>
Commit SHA:       <sha>
Author:           Avik Majumdar
Reviewer:         <independent_reviewer>
Date:             <YYYY-MM-DD>
Simulator:        Verilator 5.050
```

---

## Gate Status

| Gate | Description | Status | Evidence |
|---|---|---|---|
| 0 | Requirements complete | PASS / FAIL | VIP_DEVELOPMENT_PLAN.md |
| 1 | Architecture approved | PASS / FAIL | docs/architecture.md |
| 2 | Compilation PASS | PASS / FAIL | compile.log |
| 3 | Smoke PASS (L1) | PASS / FAIL | results/L1/summary.json |
| 4 | Directed PASS (L2) | PASS / FAIL | results/L2/summary.json |
| 5 | Random regression (L3) | PASS / FAIL | results/L3/summary.json |
| 6 | Negative tests | PASS / FAIL | results/negative/summary.json |
| 7 | Assertions | PASS / FAIL | assertions.log |
| 8 | Coverage closure | PASS / FAIL | coverage_report.html |
| 9 | Full regression (L5) | PASS / FAIL | results/L5/summary.json |
| 10 | Independent review | PASS / FAIL | <reviewer_sign> |
| 11 | SIGNOFF | PASS / NOT_READY | — |

---

## Regression Results

```
L1 Smoke:
  Total:  ___   PASS: ___   FAIL: ___   NOT_VERIFIED: ___
  Status: PASS / FAIL

L2 Directed:
  Total:  ___   PASS: ___   FAIL: ___   NOT_VERIFIED: ___
  Status: PASS / FAIL

L3 Random (seeds: ___):
  Total:  ___   PASS: ___   FAIL: ___
  Pass%:  ___%
  Status: PASS / FAIL

Negative Tests:
  Total:  ___   EXPECTED_FAILURE_DETECTED: ___   UNEXPECTED_PASS: ___
  Status: PASS / FAIL

L4 Stress (seeds: ___):
  Total:  ___   PASS: ___   FAIL: ___
  Pass%:  ___%
  Status: PASS / FAIL

L5 Full Regression:
  Total:  ___   PASS: ___   FAIL: ___
  Pass%:  ___%
  Status: PASS / FAIL
```

---

## Coverage Results

```
Functional Coverage:    ___%   (target: ≥95%)   PASS / FAIL
Code — Statement:       ___%   (target: ≥90%)   PASS / FAIL
Code — Branch:          ___%   (target: ≥85%)   PASS / FAIL
Toggle:                 ___%   (target: ≥75%)   PASS / FAIL
Assertion Exercised:    ___%   (target: ≥95%)   PASS / FAIL
Vacuous Assertions:     ___    (must be 0 or reviewed)
Disabled Assertions:    ___    (must be 0 or reviewed)
```

---

## Assertion Summary

```
Total assertions:       ___
Exercised:              ___
Vacuous:                ___   [list each with disposition]
Disabled:               ___   [list each with justification]
Formally proven:        ___
Status:                 PASS / FAIL
```

---

## Bug Summary

```
P0 open:    ___   (must be 0)
P1 open:    ___   (each must have waiver)
P2 open:    ___
Total fixed: ___
Status:     PASS / FAIL
```

---

## Simulator Compatibility

```
Verilator 5.050:   PASS | FAIL | NOT_RUN
VCS:               PASS | FAIL | NOT_RUN
Questa:            PASS | FAIL | NOT_RUN
Xcelium:           PASS | FAIL | NOT_RUN

NOTE: NOT_RUN is NOT PASS. See SIMULATOR_POLICY.md.
```

---

## Known Issues / Limitations

```
[List any known limitations, waivers, or deferred items]
[None = state "NONE"]
```

---

## Waivers

| Waiver ID | Item | Justification | Approver | Date |
|---|---|---|---|---|
| W-001 | <item> | <justification> | <name> | <date> |

---

## Independent Reviewer Statement

```
Reviewer:     <name>
Date:         <YYYY-MM-DD>

I have reviewed the signoff evidence for <vip_name> v<version>.
The regression results, coverage data, assertion summary, and bug
list have been independently examined. All gate criteria are met
as documented above.

Reviewer signature: _________________________

Final Status:   SIGNED OFF FOR VERILATOR DEVELOPMENT
                [or: NOT READY — <reason>]
```

---

## Evidence Archive

```
Regression results:    regression_db/runs/<run_id>/summary.json
Coverage report:       results/L5/coverage_merged/
Waveforms (failures):  results/<test>/seed_<N>/waveform.fst
Git tag:               <tag>
Commit SHA:            <sha>
```
