# REGRESSION POLICY
## AVIK VIP Factory · Regression Tiers · Gates · Rules

---

## Regression Tiers

### L0 — Compile (every commit, < 5 min)
```
Targets:    Compile + lint + elaboration
Gate:       Zero compile errors; zero critical lint warnings
Trigger:    Every push to any branch
Time:       < 5 minutes
```

### L1 — Smoke (every commit, < 15 min)
```
Targets:    Basic reset, basic write, basic read, basic handshake
Seeds:      Fixed (1, 2, 3)
Gate:       100% PASS
Trigger:    Every push; must pass before L2 allowed
Time:       < 15 minutes
```

### L2 — Feature (per feature PR, < 2 hours)
```
Targets:    All directed feature tests
            burst / ID / backpressure / ordering / errors
            one test per vplan scenario
Seeds:      Fixed set (1–10)
Gate:       100% PASS
Trigger:    PR to develop branch
Time:       < 2 hours
```

### L3 — Random (nightly, 4–8 hours)
```
Targets:    All constrained-random tests
Seeds:      100 random seeds per test
Gate:       ≥ 99% PASS; flaky < 1%
Trigger:    Nightly scheduled
Coverage:   Merge and report after run
Time:       4–8 hours
```

### L4 — Stress (weekly, 24 hours)
```
Targets:    Long random, max outstanding, max burst,
            max width, max concurrency, corner cases
Seeds:      1000 random seeds per stress test
Gate:       ≥ 99% PASS; coverage trending up
Trigger:    Weekly scheduled
Time:       Up to 24 hours
```

### L5 — Signoff (one-time pre-release)
```
Targets:    ALL tests: smoke + feature + random + negative + stress
Seeds:      Maximum seed count (5000+)
Coverage:   All targets must be met
Assertions: All must pass; vacuous reviewed
Gate:       100% L1/L2/negative; ≥99% L3/L4; coverage met
Trigger:    Manual — signoff decision only
Time:       48–72 hours
Review:     Independent reviewer required
```

---

## Gate Policy

```
NO GATE MAY BE SKIPPED.

L0 → L1: L0 must be PASS
L1 → L2: L1 must be PASS
L2 → L3: L2 must be PASS
L3 → L4: L3 gate met (≥99%, coverage trending)
L4 → L5: L4 gate met
L5 → SIGNOFF: Independent review complete
```

---

## Branch Policy

```
main          ← protected; merge only via PR after L5 PASS
develop       ← integration; PR after L2 PASS
feature/*     ← development; L0+L1 required before PR
hotfix/*      ← emergency fix; L1+L2 before merge to main
```

Never commit directly to `main` or `develop`.

---

## Seed Management

```
Fixed seeds (L1/L2):     1, 2, 3, 42, 137, 999, 12345
Nightly random seeds:    generated at run time; recorded in result.json
Failing seeds:           preserved permanently in regression database
Reproducer seed:         always the minimum seed that triggers the bug
```

Regression database must record every seed ever run against every test.

---

## Regression Result Database

```
regression_db/
├── runs/
│   └── <YYYYMMDD_HHMMSS>/
│       ├── summary.json
│       ├── per_test/
│       │   └── <test_name>_seed_<N>.json
│       └── coverage_merged/
├── history/
│   └── <test_name>_history.json
└── failures/
    └── <test_name>/
        └── seed_<N>/
            ├── result.json
            └── waveform.fst
```

### summary.json schema:

```json
{
  "run_id":          "<YYYYMMDD_HHMMSS>",
  "tier":            "L3",
  "vip":             "<vip_name>",
  "commit_sha":      "<sha>",
  "total":           0,
  "pass":            0,
  "fail":            0,
  "not_verified":    0,
  "blocked":         0,
  "pass_pct":        0.0,
  "flaky_pct":       0.0,
  "functional_cov":  0.0,
  "code_cov":        0.0,
  "new_failures":    [],
  "fixed_failures":  [],
  "status":          "PASS"
}
```

---

## Failure Handling

```
New failure detected
        ↓
Record: test + seed + commit SHA
        ↓
Classify: TB bug / DUT/VIP bug / Infra / Flaky
        ↓
Never delete the failing test
        ↓
Debug protocol (see DEBUG_PLAYBOOK.md)
        ↓
Root cause confirmed with evidence
        ↓
Fix implemented
        ↓
Re-run failing test (same seed) → must PASS
        ↓
Re-run all tests in same feature area
        ↓
Re-run L2 regression
        ↓
If L5: re-run full regression
```

**Never simply change the test to make it pass.**
**Never weaken an assertion to obtain PASS.**
