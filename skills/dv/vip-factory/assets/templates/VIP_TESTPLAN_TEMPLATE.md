# VIP TEST PLAN TEMPLATE
## AVIK VIP Factory · Fill in for each VIP

---

## Header

```
VIP Name:         <vip_name>
Protocol:         <protocol_name + version>
Author:           Avik Majumdar
Date:             <YYYY-MM-DD>
Version:          1.0
Status:           DRAFT / REVIEW / APPROVED
Simulator:        Verilator 5.050
```

---

## 1. Protocol Coverage Matrix

List every protocol requirement and map to test scenarios:

| Req ID | Requirement | Priority | Test(s) | Coverage Point | SVA | Status |
|---|---|---|---|---|---|---|
| R001 | <requirement> | P0 | <test_name> | <covergroup.coverpoint> | p_<name> | OPEN |

---

## 2. Test Inventory

### L1 — Smoke Tests (directed, fixed seeds)

| Test | Seed(s) | Checks | Expected Status |
|---|---|---|---|
| <vip>_smoke_test | 1,2,3 | Basic handshake, reset | PASS |

### L2 — Directed Feature Tests

| Test | Target Feature | Req ID(s) | Seeds | Expected Status |
|---|---|---|---|---|
| <vip>_write_test | Write channel | R001 | 1–10 | PASS |
| <vip>_read_test | Read channel | R002 | 1–10 | PASS |
| <vip>_burst_test | Burst types | R003 | 1–10 | PASS |
| <vip>_backpressure_test | READY deassert | R004 | 1–10 | PASS |
| <vip>_reset_test | Mid-txn reset | R005 | 1–10 | PASS |

### L3 — Random Tests

| Test | Seeds | Constraints | Expected Status |
|---|---|---|---|
| <vip>_random_test | 100 random | All legal transactions | ≥99% PASS |
| <vip>_ooo_test | 100 random | Multiple outstanding IDs | ≥99% PASS |

### Negative Tests (separate PASS definition)

| Test | Expected Violation | Checker | Expected Status |
|---|---|---|---|
| <vip>_illegal_burst_test | Reserved BURST encoding | p_burst_valid | EXPECTED_FAILURE_DETECTED |
| <vip>_4kb_crossing_test | Burst crosses 4KB | p_no_4kb_cross | EXPECTED_FAILURE_DETECTED |

### L4 — Stress Tests

| Test | Duration | Conditions | Gate |
|---|---|---|---|
| <vip>_stress_test | 1000 seeds | Max outstanding, max burst | ≥99% PASS |

---

## 3. Coverage Plan

### Functional Coverage

| Covergroup | Coverpoints | Cross | Sampling Event |
|---|---|---|---|
| <vip>_write_cg | awlen, awburst, awsize | cx_burst_len | awvalid && awready |
| <vip>_read_cg | arlen, arburst, arsize | cx_arsize_len | arvalid && arready |
| <vip>_resp_cg | bresp, rresp | — | bvalid && bready |

### Coverage Targets

| Type | Target |
|---|---|
| Functional | 95% |
| Code (statement) | 90% |
| Code (branch) | 85% |
| Toggle | 75% |
| Assertion exercised | 95% |

---

## 4. Assertion Plan

| Property Name | Description | Type | Vacuity Cover |
|---|---|---|---|
| p_<name>_stable | VALID stable without READY | Safety | COV_<name>_stable |
| p_<name>_response | Response within N cycles | Liveness | COV_<name>_req |

---

## 5. Signoff Criteria

```
L1 Smoke:         100% PASS
L2 Directed:      100% PASS
Negative tests:   100% EXPECTED_FAILURE_DETECTED
L3 Random:        ≥99% PASS (100 seeds minimum)
L4 Stress:        ≥99% PASS (1000 seeds minimum)
Functional cov:   ≥95%
Code coverage:    ≥90% (stmt), ≥85% (branch)
Assertions:       ≥95% exercised, 0 vacuous unreviewed
Open P0 bugs:     0
Open P1 bugs:     0 (or each dispositioned with waiver)
Independent review: Complete
```
