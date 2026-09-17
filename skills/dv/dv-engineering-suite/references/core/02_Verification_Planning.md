# Module 02 — Verification Planning
## Vplan · RTM · Feature Decomposition · Risk · Effort

> *"A verification plan is the contract between the design team and the verification team."*

---

## 2.1 Planning Process

```
Architecture Spec + Microarchitecture Doc
            ↓
Feature Extraction (all verifiable behaviors)
            ↓
Scenario Decomposition (per feature)
            ↓
Coverage Point Mapping (per scenario)
            ↓
SVA Property Mapping (per invariant)
            ↓
Methodology Selection (CRV/directed/formal per scenario)
            ↓
Risk Assessment (high/med/low per feature)
            ↓
Effort Estimation (person-weeks)
            ↓
Resource Planning (engineers × time)
            ↓
Regression Strategy (farm size, seed count, nightly cadence)
            ↓
Milestone Schedule (0.3 / 0.5 / 0.8 / 1.0)
            ↓
Signoff Criteria Definition
            ↓
Vplan Review and Approval
```

---

## 2.2 Feature Extraction Heuristics

When parsing a spec, identify features using these rules:

| Rule | Example |
|---|---|
| Every independent state machine = one feature | AXI read channel FSM |
| Every protocol phase = one scenario | AXI handshake, burst, response |
| Every error condition = one negative scenario | SLVERR, DECERR, timeout |
| Every configuration register = one feature set | AWCACHE fields |
| Every performance parameter = one measurement scenario | Latency, BW, OOO depth |
| Every power mode = one scenario | Power gating, retention, wake |
| Every reset domain = one scenario | POR, warm reset, subsystem reset |
| Every clock crossing = one CDC scenario | FIFO fill/drain, sync latency |

---

## 2.3 Vplan YAML Schema (production-grade)

```yaml
vplan:
  dut: <dut_name>
  rtl_version: <tag>
  author: <name>
  date: <YYYY-MM-DD>
  simulator: VCS                     # VCS | Xcelium | Questa
  uvm_version: 1.2
  protocols: [AXI4, APB4]

  coverage_targets:
    functional_pct: 95
    code_stmt_pct: 90
    code_branch_pct: 85
    code_condition_pct: 80
    toggle_pct: 75
    assertion_exercised_pct: 95
    fsm_state_pct: 90
    fsm_transition_pct: 80

  milestones:
    env_ready:         <YYYY-MM-DD>   # 0.3
    feature_complete:  <YYYY-MM-DD>   # 0.5
    coverage_closure:  <YYYY-MM-DD>   # 0.8
    signoff:           <YYYY-MM-DD>   # 1.0

  features:
    - id: F001
      name: AXI_Write_Channel
      priority: P0
      spec_ref: Sec 3.2
      risk: HIGH
      estimated_tests: 500
      methodology: constrained_random
      dependencies: []

      scenarios:
        - id: F001_S01
          name: Legal_Incr_Burst
          stimulus: constrained_random
          priority: P0
          coverage:
            - covergroup: axi_write_cg
              coverpoint: awlen_cp
              bins: [len_1, len_16, len_256]
          assertions: [p_awvalid_stable, p_wlast_correct]
          expected_bug_density: medium

        - id: F001_S02
          name: Wrap_Burst_Max_Length
          stimulus: directed
          priority: P1
          coverage:
            - covergroup: axi_write_cg
              coverpoint: awburst_cp
              bins: [WRAP]
          assertions: [p_wrap_addr_correct]
          expected_bug_density: high

        - id: F001_S03
          name: Backpressure_WREADY_Deassert
          stimulus: constrained_random
          priority: P0
          coverage:
            - covergroup: axi_bp_cg
              coverpoint: wready_bp_cp
              bins: [deassert_1cycle, deassert_10cycle, deassert_100cycle]
          assertions: [p_wvalid_stable_during_bp]
          expected_bug_density: high

        - id: F001_S04
          name: SLVERR_Response
          stimulus: directed
          priority: P1
          coverage:
            - covergroup: axi_err_cg
              coverpoint: bresp_cp
              bins: [SLVERR]
          assertions: [p_bresp_after_wlast]
          expected_bug_density: medium

  waiver_candidates:
    - item: <coverpoint>
      reason: unreachable | DFT | tie_off | dead_code
      justification: <text>
      approver: <name>

  regression:
    total_estimated_tests: 0
    seeds_per_test: 10
    farm: LSF
    parallel_jobs: 100
    nightly: true
    coverage_merge: true
```

---

## 2.4 Requirements Traceability Matrix (RTM)

Every requirement must trace to a test scenario and coverage point:

| Req ID | Requirement | Feature | Scenario(s) | Coverpoint(s) | SVA | Status |
|---|---|---|---|---|---|---|
| R001 | AWLEN valid range 0–255 | F001 | F001_S01 | awlen_cp | p_awlen_valid | PASS |
| R002 | WRAP burst address wrap | F001 | F001_S02 | awburst_cp | p_wrap_addr | OPEN |
| R003 | Backpressure handling | F001 | F001_S03 | wready_bp_cp | p_wvalid_stable | PASS |
| R004 | SLVERR response | F001 | F001_S04 | bresp_cp | p_bresp_timing | WAIVED |

RTM must be 100% PASS or WAIVED (with documentation) before milestone 1.0.

---

## 2.5 Risk Assessment Framework

### Risk Factors

| Factor | LOW | MEDIUM | HIGH |
|---|---|---|---|
| Spec clarity | Clear, complete | Some ambiguity | Incomplete/conflicting |
| RTL complexity | Simple logic | Moderate FSM | Complex pipeline/CDC |
| Protocol compliance | Single protocol | Two protocols | Multi-protocol SoC |
| Schedule pressure | Adequate time | Compressed | Extremely compressed |
| Team experience | Expert team | Mixed experience | Mostly junior |
| Reuse available | Proven TB reuse | Partial reuse | Build from scratch |
| Formal feasibility | Formal applicable | Partial | Not applicable |

### Risk → Priority Mapping

```
HIGH RISK feature → P0 priority → highest effort allocation
                              → formal verification required
                              → directed corner tests mandatory
                              → senior engineer ownership

MEDIUM RISK feature → P1 priority → standard CDV
                               → coverage-driven closure

LOW RISK feature → P2 priority → CRV sufficient
                             → waiver candidates can be considered
```

---

## 2.6 Effort Estimation

### Estimation Factors

| Activity | Rough Factor |
|---|---|
| VIP development (new, complex) | 4–8 weeks per protocol |
| VIP development (from existing) | 1–2 weeks |
| UVM env build (simple IP) | 2–4 weeks |
| UVM env build (complex SoC subsystem) | 8–16 weeks |
| Vplan (IP level) | 1 week |
| Vplan (SoC level) | 2–4 weeks |
| Scoreboard (simple) | 1 week |
| Scoreboard (complex OOO) | 2–4 weeks |
| Coverage closure (per 5% gap) | 1–2 weeks |
| Regression infrastructure | 2–4 weeks |
| Debug and bug resolution | 20–40% of total sim time |

### Estimation Template

```
Total DV effort = Σ(feature efforts) + infrastructure + debug buffer

Feature effort = env_build + vip + sequences + coverage + debug

Debug buffer = 25% of raw simulation effort
Regression buffer = 10% of total effort
Rework buffer = 15% of total effort

Headcount = Total effort (weeks) / Schedule (weeks)
```

---

## 2.7 Milestone Gates

| Milestone | Gate | Key Metrics |
|---|---|---|
| 0.3 — Env Ready | TB compiles clean; basic sanity passes | Compile: clean; sanity: ≥1 test passing |
| 0.5 — Feature Complete | All planned sequences exist; 1st coverage pass | All F-### have ≥1 test; coverage initial run |
| 0.8 — Coverage Closure | Coverage targets met; regression stable | Func ≥90%; Code ≥85%; Pass ≥95% |
| 1.0 — Signoff | All gates; risk register reviewed; board approved | All above; 0 open P0 bugs; RTM 100% |

---

## 2.8 Vplan Review Checklist

Before handing off a vplan for review:

☐ Every spec section has ≥1 feature entry
☐ Every feature has ≥1 scenario
☐ Every scenario has ≥1 coverage point
☐ Every coverage point has a sampling condition
☐ Priorities (P0/P1/P2) assigned and justified
☐ Methodology (CRV/directed/formal) stated per scenario
☐ Risk level assigned per feature
☐ Dependencies between features documented
☐ Waiver candidates pre-identified with justification
☐ Regression size estimated (tests × seeds)
☐ Coverage targets per feature stated
☐ Milestone schedule attached
☐ RTM initialized (all OPEN)
☐ Reviewers identified and scheduled
