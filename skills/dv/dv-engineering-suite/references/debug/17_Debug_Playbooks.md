# Module 17 — Debug Playbooks
## Log RCA · Waveform · Clustering · Flaky · Protocol-Specific

---

## 17.1 Debug Philosophy

> *"A verification engineer who understands architecture debugs causes.
>  One who only understands signals debugs symptoms."*
> — DV Engineering Bible Vol I, Chapter 3

**Evidence-first triage:** Classify before fixing. The checker, scoreboard,
and assertion are all suspects until proven innocent.

**Debug Priority:**
```
1. Reproduce deterministically (locked seed)
2. Narrow scope (single test, single thread)
3. Classify: TB / DUT / Infrastructure / Flaky
4. Gather evidence (waveform + log)
5. Rank hypotheses (probability-ordered)
6. Test one hypothesis at a time
7. Confirm root cause with evidence
8. Fix and add regression guard
```

---

## 17.2 UVM Log Error Classification

### Error Taxonomy

| Class | Signatures | Likely Owner |
|---|---|---|
| TB Error | Scoreboard mismatch, wrong expected value, monitor reports impossible transaction | TB (sequencer/driver/monitor/scoreboard) |
| DUT Error | Protocol violation assertion fire, incorrect response, wrong data | RTL (file bug) |
| Infrastructure | Compile error, PLI error, license timeout, LSF kill | Build/CI team |
| Flaky | Passes/fails on same seed non-deterministically | Race condition in TB or tool issue |

### Log Mining Commands
```bash
# Extract all errors with context
grep -n "UVM_ERROR\|UVM_FATAL" sim.log | head -50

# Error with ±20 lines of context
grep -A20 -B20 "UVM_ERROR" sim.log | head -200

# Get test info
grep -E "UVM_TESTNAME|ntb_random_seed|Simulation PASS|Simulation FAIL" sim.log

# Count error clusters
grep "UVM_ERROR" sim.log | sed 's/@ [0-9]*ns//' | sort | uniq -c | sort -rn | head -20

# Extract failing test + seed
grep "SEED\|TESTNAME\|UVM_FATAL" failed_run.log
```

---

## 17.3 Seven-Step Debug Protocol

```
Step 1: EXTRACT
  grep ±20 lines around UVM_ERROR/FATAL
  Record: test name, seed, timestamp, error message

Step 2: CLASSIFY
  TB / DUT / Infra / Flaky
  Rule out TB first — always

Step 3: RANK HYPOTHESES
  List 3–5 ordered by probability
  Never start with RTL fix if TB is suspect

Step 4: IDENTIFY SIGNALS
  Which protocol signals, FSM states, and counters are relevant?

Step 5: GATHER EVIDENCE
  Dump waveform (DUMP=1 or equivalent)
  grep target signals from log
  Check scoreboard internal state

Step 6: TEST ONE HYPOTHESIS
  Change one variable only
  Rerun with same seed

Step 7: CONFIRM + GUARD
  When root cause confirmed: file bug or fix TB
  Add SVA or coverage point as regression guard
  Document in areas file
```

---

## 17.4 Protocol-Specific Debug Anchors

### AXI4 Debug
```bash
# Key signals to trace first
AWVALID AWREADY AWADDR AWLEN AWBURST AWSIZE AWID
WVALID  WREADY  WDATA  WSTRB WLAST
BVALID  BREADY  BRESP  BID
ARVALID ARREADY ARADDR ARLEN ARBURST ARID
RVALID  RREADY  RDATA  RRESP RLAST   RID

# Common failure patterns
"timeout waiting for BVALID"   → BVALID stall: outstanding counter, DUT response dropped
"WLAST mismatch"               → beat count vs AWLEN+1 mismatch
"ID mismatch"                  → BID/RID not matching AWID/ARID
"BRESP = SLVERR unexpected"    → address decode issue or DUT error injection
"WVALID deasserted mid-burst"  → protocol violation by driver (TB bug)
```

### AHB Debug
```bash
# Key signals
HSEL HADDR HTRANS HWRITE HSIZE HBURST HWDATA HRDATA HREADYOUT HRESP

# Common failures
"HREADYOUT stuck LOW"           → slave not releasing bus
"Single-cycle ERROR response"   → HRESP=ERROR without HREADYOUT=0 first cycle
"HTRANS missing SEQ in burst"   → master not continuing burst correctly
```

### APB Debug
```bash
# Key signals
PSEL PENABLE PWRITE PADDR PWDATA PRDATA PREADY PSLVERR

# Common failures
"PREADY stuck LOW"              → slave timeout
"PSLVERR without PENABLE"       → spurious error assertion
"PENABLE not deasserted"        → master not returning to IDLE
```

### CHI Debug
```bash
# Key signals
TXREQFLIT TXREQFLITV TXREQLCRDV
RXDATFLIT RXDATFLITV
TXRSPFLIT TXRSPFLITV

# Common failures
"No credit available"           → LCRDV not returned by HN
"TxnID collision"               → outstanding limit exceeded
"RetryAck without PCrdGrant"    → requester must wait for grant before retry
```

---

## 17.5 Waveform Debug — Verdi TCL Recipes

### AXI Full-Channel Setup
```tcl
# Add complete AXI write channel
proc add_axi_write {path} {
  foreach sig {
    AWVALID AWREADY AWADDR AWLEN AWBURST AWSIZE AWID AWCACHE AWPROT
    WVALID WREADY WDATA WSTRB WLAST
    BVALID BREADY BRESP BID
  } { add wave -noupdate -label $sig $path/$sig }
}

# Add complete AXI read channel
proc add_axi_read {path} {
  foreach sig {
    ARVALID ARREADY ARADDR ARLEN ARBURST ARID
    RVALID RREADY RDATA RRESP RLAST RID
  } { add wave -noupdate -label $sig $path/$sig }
}

# Zoom to error timestamp
proc zoom_to_error {time_ns margin_ns} {
  wave zoom -from [expr {$time_ns - $margin_ns}]ns \
            -to   [expr {$time_ns + $margin_ns}]ns
}

# Usage
add_axi_write /tb_top/dut/axi_write_if
zoom_to_error 4523 200
```

### Find First Assertion of Signal
```tcl
# Find first posedge of BVALID
set t [lindex [find signal -edge posedge /tb_top/dut/BVALID] 0]
puts "First BVALID at: $t"
wave zoom -from [expr {$t - 50}]ns -to [expr {$t + 100}]ns
```

---

## 17.6 Failure Clustering — Manual Method

When automated clustering isn't available:

```bash
# Step 1: Count distinct error patterns
grep "UVM_ERROR" *.log | \
  sed 's/@[0-9]*ns//' | \
  sed 's/0x[0-9a-f]*/ADDR/g' | \
  sed 's/[0-9]\{4,\}/NUM/g' | \
  sort | uniq -c | sort -rn | head -20

# Step 2: Find minimal reproducer per cluster
# Take the lowest seed from each cluster
grep "SEED" cluster1_logs/*.log | sort -t: -k2 -n | head -1

# Step 3: Cluster report format
```

```yaml
failure_clusters:
  - name: BVALID_Timeout
    count: 850
    pct: 56.7
    example_seed: 42
    error_pattern: "Slave timeout waiting for BVALID — outstanding=N"
    classification: DUT_SUSPECT      # rule out TB-1 first
    status: OPEN

  - name: Addr_Decode_Error
    count: 420
    pct: 28.0
    example_seed: 137
    error_pattern: "Scoreboard: unexpected DECERR at addr=ADDR"
    classification: TB_SUSPECT       # check address map in env cfg
    status: ROOT_CAUSING
```

---

## 17.7 Flaky Test Detection

**Flaky:** passes on some runs, fails on others with the same seed.

```bash
# Run same seed 10 times
for i in $(seq 1 10); do
  make run SEED=42 TEST=my_test 2>&1 | \
    grep -E "PASS|FAIL" >> flaky_check.log
done
cat flaky_check.log | sort | uniq -c
```

### Flaky Root Causes

| Cause | Debug Approach |
|---|---|
| Race condition in TB (blocking vs non-blocking) | grep for `=` vs `<=` in monitor/checker |
| Phase objection race | Add `#1ns` drain after sequence end |
| Non-deterministic UVM factory global state | Ensure factory is clean at test start |
| `@(posedge clk)` vs `@(negedge clk)` sampling | Standardize monitor sampling edge |
| LSF slot-dependent timing | Run locally to rule out farm variability |
| VCS/Xcelium scheduler non-determinism | Try `-timescale_override`, check delta-cycle issues |

---

## 17.8 Debug QA Checklist

☐ Failure reproduced deterministically (locked seed confirmed)
☐ Error classified: TB / DUT / Infra / Flaky — before any fix
☐ TB ruled out before RTL engineer engaged
☐ Root cause confirmed with waveform or log evidence
☐ Fix implemented and regression confirmed
☐ SVA or coverage guard added as regression protection
☐ Bug filed in tracker with: seed, test, error, root cause, fix CL
☐ Cluster report updated with status change
☐ Similar historical failures cross-referenced
