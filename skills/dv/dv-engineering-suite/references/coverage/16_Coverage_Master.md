# Module 16 — Coverage Master
## Functional · Code · Toggle · FSM · Assertion · Closure · Analytics

---

## 16.1 Coverage Philosophy

Coverage is the **quantitative language of verification completeness**.
A coverage point that is not reached = unknown behavior under that condition.

**Coverage-Driven Verification (CDV) loop:**
```
Write coverage model (from vplan)
          ↓
Run constrained-random regression
          ↓
Measure coverage → URG/IMC report
          ↓
Analyze holes
          ↓
Classify: missing stimulus / unreachable / wrong sampling
          ↓
Generate directed tests or refine constraints
          ↓
Re-run → convergence → signoff
```

---

## 16.2 Coverage Types Reference

| Type | What it measures | Tool flag (VCS) | Target |
|---|---|---|---|
| Functional | Feature completeness vs. vplan | N/A (userspace SV) | 95% |
| Line/Statement | Lines of RTL executed | `-cm line` | 90% |
| Branch | All RTL branch outcomes | `-cm branch` | 85% |
| Condition | Each sub-expression evaluated | `-cm cond` | 80% |
| Toggle | Each net toggled 0→1 and 1→0 | `-cm tgl` | 75% |
| FSM state | Each FSM state reached | `-cm fsm` | 90% |
| FSM transition | Each FSM state→state arc | `-cm fsm` | 80% |
| Assertion | SVA antecedent triggered | `-cm assert` | 95% |

### VCS Coverage Flags
```bash
# Full coverage collection
vcs -cm line+cond+tgl+fsm+branch+assert \
    -cm_dir ./coverage_db \
    -cm_name test_${TEST_NAME}_seed_${SEED}

# Merge coverage databases
urg -dir ./coverage_db -report ./urg_report -format text
```

### Xcelium
```bash
xrun -coverage all -covdb coverage_db
imc -load coverage_db -report func_cov.html
```

---

## 16.3 Functional Coverage — Covergroup Design

### Anatomy of a Production Covergroup

```systemverilog
covergroup axi_write_cg @(posedge clk iff (awvalid && awready));
  // Instance-level granularity (required for per-master tracking)
  option.per_instance = 1;
  option.comment      = "AXI Write Address Channel Coverage";
  option.goal         = 100;

  // ─── Coverpoints ───────────────────────────────────────────

  // Burst length bins
  cp_awlen: coverpoint awlen {
    option.auto_bin_max = 0;               // disable auto bins
    bins len_1       = {8'h00};            // single beat
    bins len_2       = {8'h01};
    bins len_4       = {8'h03};
    bins len_8       = {8'h07};
    bins len_16      = {8'h0F};
    bins len_64      = {8'h3F};
    bins len_256     = {8'hFF};            // maximum
    bins len_other   = default;
    illegal_bins len_reserved = {[8'h10:8'hFE]};  // reserved range
  }

  // Burst type
  cp_awburst: coverpoint awburst {
    bins FIXED = {2'b00};
    bins INCR  = {2'b01};
    bins WRAP  = {2'b10};
    illegal_bins RESERVED = {2'b11};
  }

  // Transfer size
  cp_awsize: coverpoint awsize {
    bins byte_1   = {3'h0};
    bins byte_2   = {3'h1};
    bins byte_4   = {3'h2};
    bins byte_8   = {3'h3};
    bins byte_16  = {3'h4};
    bins byte_32  = {3'h5};
    bins byte_64  = {3'h6};
    bins byte_128 = {3'h7};
  }

  // Address alignment
  cp_addr_align: coverpoint awaddr[5:0] {
    bins aligned   = {6'h00};             // naturally aligned
    bins unaligned = {[6'h01:6'h3F]};
  }

  // ─── Cross Coverage ─────────────────────────────────────────

  // Burst type × Length — primary cross
  cx_burst_len: cross cp_awburst, cp_awlen {
    // WRAP: only valid with power-of-2 lengths
    illegal_bins wrap_invalid =
      binsof(cp_awburst.WRAP) && binsof(cp_awlen.len_other);
    // FIXED with len > 16 is unusual — track separately
    bins fixed_long =
      binsof(cp_awburst.FIXED) && (binsof(cp_awlen.len_64)
                                || binsof(cp_awlen.len_256));
  }

  // Size × Length — data volume scenarios
  cx_size_len: cross cp_awsize, cp_awlen;

  // Size × Alignment
  cx_size_align: cross cp_awsize, cp_addr_align;

endgroup
```

### Covergroup Instantiation
```systemverilog
class axi_coverage extends uvm_subscriber#(axi_seq_item);
  `uvm_component_utils(axi_coverage)

  axi_write_cg   m_write_cg;
  axi_read_cg    m_read_cg;
  axi_backpressure_cg m_bp_cg;

  // Sampled signals — set by write() function
  logic [7:0]  awlen;
  logic [1:0]  awburst;
  logic [2:0]  awsize;
  logic [31:0] awaddr;
  logic        clk;

  function void build_phase(uvm_phase phase);
    m_write_cg = new();
    m_read_cg  = new();
    m_bp_cg    = new();
  endfunction

  function void write(axi_seq_item t);
    // Copy transaction fields to sampled signals
    awlen   = t.awlen;
    awburst = t.awburst;
    awsize  = t.awsize;
    awaddr  = t.awaddr;
    // Sampling happens automatically via @(posedge clk iff ...) in cg
    // For software-sampled covergroups, call .sample() explicitly:
    m_write_cg.sample();
  endfunction
endclass
```

---

## 16.4 Coverage Exclusion Management

### Exclusion File Format (VCS)
```
// Line exclusion
FILEINFO : filename.sv 123 // dead code — reset-only path
// Branch exclusion
BRANCHINFO : filename.sv 456 FT // false branch — never false
// Toggle exclusion
TOGGLEINFO : filename.sv.dut.signal // tied-off port
// Condition exclusion
CONDINFO : filename.sv 789 FT
```

### Exclusion Justification Template
```yaml
exclusions:
  - id: EXC-001
    type: line
    file: arbiter.sv
    line: 234
    justification: "Dead code path — only reachable via RTL bug; intentionally excluded"
    approver: <name>
    date: <YYYY-MM-DD>

  - id: EXC-002
    type: toggle
    signal: dut.tie_high_port
    justification: "Port permanently tied HIGH in all configurations; 0 value impossible"
    approver: <name>
    date: <YYYY-MM-DD>
```

**Rule:** Never increase coverage by adding exclusions without documented justification.

---

## 16.5 Coverage Closure Protocol

### Step 1 — Classify the Hole

| Hole Type | Description | Resolution |
|---|---|---|
| Missing stimulus | Valid scenario not yet reached by CRV | Add directed test or refine constraints |
| Unreachable | Architectural impossibility | Waiver with justification |
| Wrong sampling | Covergroup fires at wrong time | Fix sampling condition |
| Wrong bin | Bin boundary doesn't match spec | Fix bin definition |
| Weight = 0 | Accidentally disabled | Fix option.weight |
| RTL bug | RTL prevents reaching the state | File bug, re-verify after fix |

### Step 2 — Root Cause Drill-Down
```
Coverage hole: awburst=WRAP, awlen=255 → 0 hits

Questions:
1. Is WRAP+len=255 architecturally legal?   → Check spec
2. Does the constraint allow it?             → Check constraint in sequence
3. Does the driver correctly drive it?      → Check driver
4. Does the monitor capture it?             → Check monitor
5. Does the covergroup sample correctly?    → Check sampling event
6. Does the DUT accept it?                  → Check RTL
```

### Step 3 — Generate Directed Test

```systemverilog
// Coverage-gap-driven directed sequence
class axi_wrap_max_seq extends axi_base_seq;
  `uvm_object_utils(axi_wrap_max_seq)

  task body();
    axi_seq_item req;
    req = axi_seq_item::type_id::create("req");
    start_item(req);
    if (!req.randomize() with {
      awburst == 2'b10;        // WRAP
      awlen   == 8'hFF;        // 256 beats — maximum WRAP
      awsize  == 3'h2;         // 4 bytes per beat
      awaddr  == 32'h0000_0000;// aligned to burst boundary
    }) `uvm_fatal(get_name(), "Randomization failed")
    finish_item(req);
  endtask
endclass
```

### Step 4 — Constraint Refinement
```systemverilog
// Before closure: equal weight on all burst types
constraint c_burst { awburst dist {2'b00:=10, 2'b01:=80, 2'b10:=10}; }

// After analysis shows WRAP under-sampled: increase weight
constraint c_burst_closure { awburst dist {2'b00:=5, 2'b01:=60, 2'b10:=35}; }
```

---

## 16.6 Coverage Reporting

### URG (VCS Coverage Report)
```bash
# Generate HTML + text report
urg -dir ./coverage_db -report ./urg_report -format both

# Merge multiple runs
urg -dir run1/coverage_db -dir run2/coverage_db \
    -report ./merged_report -format both

# Per-test breakdown
urg -dir ./coverage_db -show tests -report ./per_test_report
```

### Coverage Report Interpretation
```
Functional coverage summary:
  Groups   : 12
  Covered  : 11     91.7%
  Failed   : 1

Failed covergroup: axi_write_cg
  cp_awburst  100.0%
  cp_awlen     87.5%   ← HOLE: len_256 = 0 hits
  cp_awsize   100.0%
  cx_burst_len 85.2%   ← HOLES: WRAP×len_256, WRAP×len_64
```

### Coverage Analytics (from Agentic AI DV Architecture)
```yaml
# AI Coverage Analysis Agent output
coverage_analysis:
  overall_functional_pct: 87.3
  trend:
    week_minus_2: 78.1
    week_minus_1: 83.7
    current:      87.3
    velocity:     +4.6%/week
    estimated_closure: 3 weeks at current velocity

  holes:
    - coverpoint: axi_write_cg.cp_awlen
      bin: len_256
      hits: 0
      estimated_tests_to_close: 5
      recommended_action: directed_test
      test_class: axi_wrap_max_seq

    - coverpoint: axi_write_cg.cx_burst_len
      bin: WRAP_x_len_256
      hits: 0
      estimated_tests_to_close: 3
      recommended_action: constraint_weight
      constraint_change: "awburst dist {WRAP:=40}; awlen dist {8'hFF:=30}"
```

---

## 16.7 Coverage QA Checklist

☐ Every vplan feature has ≥1 covergroup
☐ Every covergroup has an explicit sampling event (not free-running)
☐ Cross bins are named (not anonymous)
☐ `option.per_instance = 1` set where instance-level granularity needed
☐ Exclusions documented in exclusion file with justification
☐ No holes waived without RTM update
☐ URG report generated and reviewed
☐ Coverage trend measured (not just snapshot)
☐ All cross bins that are architecturally impossible marked illegal
☐ Functional coverage ≥ 95% before signoff
☐ Code coverage exclusions reviewed by RTL engineer
