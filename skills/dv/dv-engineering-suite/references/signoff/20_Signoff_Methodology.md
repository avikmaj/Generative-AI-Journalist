# Module 20 — Signoff Methodology
## Evidence Package · Milestone Gates · Risk Register · Review Board

For agent coordination, use the SUPER-BRAIN DV operating contract (`knowledge/dv/agentic_ai_dv_architecture.md` in the repository; not bundled inside this skill). REVIEW_AGENT evaluates the exact requirement, RTL, DV, tool, and configuration snapshot and may return work to the appropriate loop. A review of bug reproduction or documentation does not permit design advancement or signoff. Changes invalidate affected results and reviews until rerun and independently checked. The orchestrator records readiness; final signoff and waiver acceptance belong to the project's human engineering authority.

The numeric targets and populated status fields below are illustrative planning templates, not measured project results or universal acceptance criteria. Set project-specific targets from the approved verification plan. Use null with NOT_MEASURED or NOT_RUN for unavailable evidence; never initialize a live project's unknown metrics as zero or COMPLETE.

---

## 20.1 Signoff Philosophy

> *"Verification is complete not when simulation stops, but when the evidence
>  is sufficient, the risks are understood, the residuals are accepted,
>  and the engineering team can stand behind the decision."*
> — DV Engineering Bible Vol I, Chapter 47

Signoff is a **conscious engineering decision**, not a coverage number.
It requires: documented evidence + risk assessment + acceptance + board approval.

---

## 20.2 Milestone Gates

| Milestone | Gate Name | Entry Criteria | Key Metrics |
|---|---|---|---|
| 0.3 | Environment Ready | TB compiles clean; basic sanity passes | Compile: clean; ≥1 sanity test passing |
| 0.5 | Feature Complete | All planned test classes exist; first coverage run | All F-### have ≥1 test; initial coverage generated |
| 0.8 | Coverage Closure | Coverage targets met; regression stable | Func ≥90%; Code ≥85%; Pass ≥95%; Flaky <1% |
| 1.0 | Signoff | All above + risk reviewed + board approved | All targets; 0 P0 bugs; RTM 100%; Board approval |

---

## 20.3 Coverage Targets at Signoff

| Coverage Type | Minimum Gate | Ideal Target |
|---|---|---|
| Functional | 95% | 98–100% |
| Code — Statement | 90% | 95% |
| Code — Branch | 85% | 90% |
| Code — Condition | 80% | 85% |
| Toggle | 75% | 85% |
| FSM State | 90% | 95% |
| FSM Transition | 80% | 90% |
| Assertion (exercised) | 95% | 98–100% |

**Never self-signoff on coverage alone.** Coverage shows how much was tested,
not whether what was tested is correct.

---

## 20.4 Signoff Evidence Package

```yaml
signoff_evidence_package:
  dut: <dut_name>
  rtl_version: <tag>
  dv_lead: <name>
  date: <YYYY-MM-DD>
  board_decision: pending

  # 1. Requirements Traceability Matrix
  requirements_traceability:
    status: COMPLETE
    total_requirements: 0
    pass_count: 0
    waived_count: 0
    open_count: 0         # must be 0 for signoff
    matrix_location: <path/RTM.xlsx>

  # 2. Functional Coverage
  functional_coverage:
    status: COMPLETE
    overall_pct: 0.0
    target_pct: 95.0
    holes_open: 0
    holes_waived: 0
    waiver_count: 0
    report_location: <path/urg_report/>

  # 3. Code Coverage
  code_coverage:
    status: COMPLETE
    statement_pct: 0.0   # target ≥90
    branch_pct:    0.0   # target ≥85
    condition_pct: 0.0   # target ≥80
    toggle_pct:    0.0   # target ≥75
    exclusions_documented: false
    exclusion_file: <path/cm_exclusions.el>

  # 4. Assertion Summary
  assertions:
    total: 0
    exercised: 0
    vacuous: 0           # must all be reviewed
    disabled: 0          # must all be reviewed — none allowed without waiver
    formally_proven: 0

  # 5. Regression Summary (minimum 5 consecutive stable runs)
  regression:
    runs_included: 5
    avg_pass_pct: 0.0    # target ≥99
    avg_flaky_pct: 0.0   # target <1
    last_run_pass_pct: 0.0
    open_deterministic_failures: 0  # must be 0

  # 6. Bug Summary
  bugs:
    p0_open: 0           # must be 0 — no exceptions
    p1_open: 0           # each needs documented disposition
    p2_open: 0
    total_closed: 0
    escape_count: 0
    mttd_days: 0.0
    mttr_days: 0.0

  # 7. Performance Results
  performance:
    latency_avg_ns: 0.0
    latency_target_ns: 0.0
    bandwidth_gbps: 0.0
    bandwidth_target_gbps: 0.0
    targets_met: false

  # 8. Risk Register
  risk_register:
    total_open: 0
    residuals_accepted: false
    risks: []
    # Each risk entry:
    # - id: RISK-001
    #   description: <text>
    #   probability: LOW|MED|HIGH
    #   impact: LOW|MED|HIGH
    #   mitigation: <text>
    #   residual_risk: ACCEPTED|OPEN
    #   owner: <name>

  # 9. Waiver Log
  waiver_log:
    total: 0
    waivers: []
    # Each waiver:
    # - id: W-001
    #   type: coverage|assertion|bug|exclusion
    #   item: <name>
    #   justification: <text>
    #   approver: <name>
    #   date: <YYYY-MM-DD>

  # 10. Review Board
  review_board:
    scheduled_date: <YYYY-MM-DD>
    participants:
      - {role: DV Lead,          name: <name>}
      - {role: RTL Lead,         name: <name>}
      - {role: Design Architect, name: <name>}
      - {role: DFT Lead,         name: <name>}
      - {role: Program Manager,  name: <name>}
    agenda:
      - Requirements: "All traced; waivers approved"
      - Coverage:     "Targets met; holes classified"
      - Regression:   "≥5 stable runs; failures resolved"
      - Assertions:   "All exercised; vacuous reviewed"
      - Bugs:         "P0=0; P1 dispositioned"
      - Performance:  "Targets met"
      - Risk:         "Register reviewed; residuals accepted"
      - Decision:     "approved|approved_with_conditions|not_approved"
    decision: pending
```

---

## 20.5 Tapeout Readiness Checklist

```
VERIFICATION
☐ Requirements traceability: 100% PASS or WAIVED
☐ Functional coverage: ≥95% (waivers approved)
☐ Code coverage: stmt≥90%, branch≥85%, condition≥80%
☐ Toggle coverage: ≥75% (hard-reset resets reviewed)
☐ Assertion coverage: ≥95% exercised; 0 vacuous unreviewed
☐ Regression: ≥99% pass; <1% flaky; 5 consecutive stable runs
☐ P0 bugs: 0 open
☐ P1 bugs: all dispositioned with waiver
☐ Performance targets: met
☐ Risk register: reviewed; residuals accepted

STATIC / FORMAL
☐ CDC signoff: Spyglass/Meridian clean (or waivers approved)
☐ RDC signoff: clean or waivers approved
☐ Lint: clean or waivers approved
☐ Formal connectivity: all paths proven

POWER / DFT / SECURITY
☐ Low-power verification: UPF/CPF compliant
☐ DFT verification: ATPG coverage meets target
☐ Security verification: threat model coverage

DOCUMENTATION
☐ Vplan final version checked in
☐ RTM final version checked in
☐ Bug summary report generated
☐ Coverage report archived
☐ Regression report archived
☐ Risk register final version
☐ Waiver log approved and archived
☐ Review board minutes recorded

PROCESS
☐ Review board held with quorum
☐ Decision: approved (or approved with conditions)
☐ Conditions (if any) tracked and resolved before tape-in
☐ Signoff package archived to project record
```

---

## 20.6 Post-Tapeout Feedback Loop

```
Tapeout
    ↓
Silicon bring-up
    ↓
Post-silicon validation
    ↓
Escape analysis: which pre-silicon tests would have caught each escape?
    ↓
Lessons learned:
  - Which coverage model missed the escape scenario?
  - Which assumption in vplan was wrong?
  - Which corner case was under-weighted?
    ↓
Process improvements for next project:
  - New coverage points added
  - New negative test classes
  - New SVA properties
  - Updated risk model
```

**The feedback loop separates organizations that improve from those that repeat mistakes.**

---

## 20.7 Common Signoff Mistakes

| Mistake | Consequence |
|---|---|
| Signoff on coverage number alone | Residual risks unquantified |
| Waiving holes without justification | Silent risk acceptance |
| Not reviewing vacuous assertions | False confidence in assertion coverage |
| Signing off with unstable regression | Unreliable pass rate |
| Self-signoff (no independent review) | Conflicts of interest undetected |
| Not updating RTM before signoff | Requirements untraced |
| Skipping board due to schedule | No independent technical review |
| Not archiving signoff package | No evidence trail for escapes |
