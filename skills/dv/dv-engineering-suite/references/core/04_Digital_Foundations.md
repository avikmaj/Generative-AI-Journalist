# Module 04 — Digital Foundations
## FSMs · CDC · RDC · Pipelines · Reset · Timing

---

## 4.1 FSM Verification

```
For every FSM in the DUT, verify:
- All states reachable (cover property per state)
- All legal transitions exercised (cover property per arc)
- All illegal transitions rejected (assert property)
- Reset takes FSM to correct initial state
- Dead states: states with no exit — find and report
- Unreachable states: no entry path — waiver candidate
```

```systemverilog
// Cover all states
COV_IDLE:    cover property(@(posedge clk) state == S_IDLE);
COV_ACTIVE:  cover property(@(posedge clk) state == S_ACTIVE);
COV_ERROR:   cover property(@(posedge clk) state == S_ERROR);
COV_DRAIN:   cover property(@(posedge clk) state == S_DRAIN);

// Assert no invalid encoding
P_STATE_VALID: assert property(@(posedge clk) state inside {S_IDLE, S_ACTIVE, S_ERROR, S_DRAIN})
  else `uvm_error("FSM", "Invalid state encoding");

// Cover transitions
COV_IDLE_TO_ACTIVE: cover property(@(posedge clk) (state == S_IDLE) ##1 (state == S_ACTIVE));
```

## 4.2 Clock Domain Crossing (CDC)

```
CDC violation classes:
1. Missing synchronizer          — async data crossing without sync flops
2. Combinational logic in path   — logic between two sync flops
3. Reconvergence                 — two paths from same CDC source merge
4. Multi-bit CDC                 — multiple bits crossing without gray code
5. Glitch generation             — combinational glitch propagates to CDC

CDC verification approach:
1. Structural CDC analysis: Spyglass CDC, Meridian CDC — find violations
2. Simulation: inject randomized clock-phase relationships
3. Formal CDC: prove synchronizer correctness
4. SVA: check that multi-bit buses use gray coding
```

## 4.3 Reset Verification

```
Reset scenarios (must be in vplan):
- Power-on reset: all state elements to known values
- Warm reset: selected state preserved, others reset
- Reset during active transaction: DUT must recover cleanly
- Reset assertion width: minimum assertion time
- Reset de-assertion timing: synchronous vs asynchronous
- Multiple reset domains: correct sequencing
- Reset storm: rapid assertion/de-assertion cycles

Directed reset sequence:
1. Assert reset for N cycles
2. Drive traffic (optional — for mid-transaction reset)
3. Assert reset again
4. De-assert reset
5. Verify all state returns to spec-defined reset values
6. Re-run functional tests — must pass identically
```

## 4.4 Pipeline Verification

```
Pipeline depth = D stages
Key scenarios:
- Back-to-back transactions (no bubble)
- Single transaction (isolated)
- Stall injection at each stage
- Flush during stall
- Data dependencies (if bypass/forwarding exists)
- Pipeline fill and drain

Coverage model:
covergroup pipeline_cg @(posedge clk);
  cp_occupancy: coverpoint pipeline_occupancy {
    bins empty  = {0};
    bins half   = {[1:D/2]};
    bins full   = {D};
  }
  cp_stall: coverpoint stall_cycles {
    bins no_stall   = {0};
    bins short_stall = {[1:4]};
    bins long_stall  = {[5:$]};
  }
endgroup
```
