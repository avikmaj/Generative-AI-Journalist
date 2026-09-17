# PASS / FAIL POLICY
## AVIK VIP Factory · Authoritative Definition Document

---

## The Core Problem This Policy Solves

An AI assistant can inspect code, reason about expected behavior, and
write "PASS" — all without running a single simulation. This produces
**false confidence**. This policy makes that impossible by defining PASS
exclusively in terms of **observable simulator evidence**.

---

## Status Taxonomy

| Status | Definition | Evidence Required |
|---|---|---|
| `PASS` | Simulator ran; all checks passed | All 10 requirements below |
| `FAIL` | Simulator ran; one or more checks failed | Exit code, error log, failing check |
| `EXPECTED_FAILURE_DETECTED` | Negative test: expected violation was caught | Assertion/checker fired as expected |
| `UNEXPECTED_PASS` | Negative test: expected violation NOT caught | Treat as FAIL — DUT/VIP defect |
| `NOT_VERIFIED` | Simulator did not run, or evidence is missing | Document what is missing |
| `BLOCKED` | Cannot run — dependency or environment missing | Document blocker and owner |
| `SIGNED_OFF` | Independent review complete; all gates passed | Signoff document with reviewer name |

---

## The 10 PASS Requirements

A test is PASS **only when all 10 are true**:

```
Requirement 1:  Simulator actually executed the test
                Evidence: process launched, log file exists

Requirement 2:  Simulator returned expected success status
                Evidence: exit code = 0 (or protocol-specific success)

Requirement 3:  Checker / scoreboard verified expected behavior
                Evidence: scoreboard report shows 0 errors

Requirement 4:  No unexpected UVM_ERROR
                Evidence: log shows "UVM_ERROR : 0"

Requirement 5:  No UVM_FATAL
                Evidence: log shows "UVM_FATAL : 0"

Requirement 6:  Required assertions passed
                Evidence: assertion report shows 0 failures

Requirement 7:  Required functional coverage collected
                Evidence: coverage report shows ≥ target%

Requirement 8:  Test name and seed recorded
                Evidence: result.json contains test + seed fields

Requirement 9:  Result stored in regression database
                Evidence: results/<test>/seed_<N>/result.json exists

Requirement 10: Result is reproducible
                Evidence: re-run with same seed produces same outcome
```

---

## Negative Test PASS Definition

A negative test exercises **illegal or error conditions**. Its PASS
means the DUT/VIP **correctly detected and reported** the violation.

```
Positive test PASS:  No errors observed (correct operation)
Negative test PASS:  Expected error detected (correct error handling)
```

### Example — AXI4 4KB boundary crossing:

```json
{
  "test":     "axi4_illegal_4kb_crossing_test",
  "seed":     827361,
  "expected": "PROTOCOL_VIOLATION",
  "observed": "PROTOCOL_VIOLATION",
  "checker":  "axi4_protocol_checker assertion P_NO_4KB_CROSSING fired",
  "status":   "PASS"
}
```

### Counter-example — same test, checker missed it:

```json
{
  "test":     "axi4_illegal_4kb_crossing_test",
  "seed":     827361,
  "expected": "PROTOCOL_VIOLATION",
  "observed": "NO_ERROR",
  "checker":  "axi4_protocol_checker — assertion NOT fired",
  "status":   "UNEXPECTED_PASS"
}
```

`UNEXPECTED_PASS` = the checker failed to catch the violation = **this is a FAIL**.

---

## NOT_VERIFIED Rules

The following conditions produce `NOT_VERIFIED` (never silently convert to PASS):

```
- Simulator not installed or not found
- Compilation failed (elaboration error)
- Simulator crashed before test completed
- Log file missing or empty
- Result artifact missing
- Checker/scoreboard not instantiated in the test
- Coverage collection not enabled
- Test ran but no UVM report summary found
- Seed not recorded
- Waveform required but not generated (for debug tests)
```

---

## Result Artifact Schema

Every test execution must produce this exact structure:

```
results/
└── <test_name>/
    └── seed_<N>/
        ├── result.json       ← machine-readable verdict
        ├── transcript.log    ← full simulator output
        ├── scoreboard.log    ← scoreboard summary
        ├── assertions.log    ← assertion pass/fail list
        ├── coverage.dat      ← coverage database
        ├── waveform.fst      ← waveform (for FAIL always; PASS optional)
        └── metadata.json     ← build info, commit SHA, timestamp
```

### result.json schema:

```json
{
  "test":                 "<test_name>",
  "seed":                 0,
  "simulator":            "verilator",
  "simulator_version":    "5.050",
  "commit_sha":           "<git_sha>",
  "timestamp":            "<ISO-8601>",
  "status":               "PASS",
  "exit_code":            0,
  "uvm_errors":           0,
  "uvm_fatals":           0,
  "assertion_failures":   0,
  "scoreboard_errors":    0,
  "functional_coverage":  0.0,
  "code_coverage":        0.0,
  "runtime_seconds":      0.0,
  "expected":             "NORMAL",
  "observed":             "NORMAL",
  "waveform":             "waveform.fst",
  "notes":                ""
}
```

### metadata.json schema:

```json
{
  "vip":              "<vip_name>",
  "vip_version":      "<version>",
  "commit_sha":       "<git_sha>",
  "branch":           "<branch>",
  "simulator":        "verilator",
  "simulator_version": "5.050",
  "uvm_version":      "<version>",
  "build_flags":      [],
  "run_flags":        [],
  "host":             "<hostname>",
  "os":               "<os>",
  "timestamp":        "<ISO-8601>"
}
```

---

## Coverage Targets at PASS

| Coverage Type | Minimum for PASS | Target |
|---|---|---|
| Functional | 95% | 98% |
| Code (line) | 90% | 95% |
| Code (branch) | 85% | 90% |
| Toggle | 75% | 85% |
| Assertion exercised | 95% | 98% |

Coverage below minimum = `NOT_VERIFIED` for signoff gate (Coverage Closure).

---

## What Claude Must Never Do

```
FORBIDDEN:
× Write "PASS" without running the simulator
× Infer PASS from compilation success
× Infer PASS from code inspection
× Infer PASS from reasoning about expected behavior
× Convert NOT_VERIFIED to PASS
× Delete or modify a failing test to make it appear to pass
× Weaken an assertion to obtain PASS without documented justification
× Claim simulator portability without running that simulator
× Report a seed without recording it in result.json
```
