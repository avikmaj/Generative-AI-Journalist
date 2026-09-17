# Module 15 — Formal Verification and SVA
## Properties · Assumptions · Liveness · Safety · Apps · Debug

---

## 15.1 SVA — SystemVerilog Assertions

### Assertion Types

| Type | Keyword | Evaluated | Use |
|---|---|---|---|
| Immediate | `assert` | Procedurally | Quick checks in TB |
| Concurrent | `assert property` | Every clock cycle | Protocol invariants |
| Cover | `cover property` | Every clock cycle | Prove reachability |
| Assume | `assume property` | Formal tool — constrains inputs | Formal assumptions |

---

## 15.2 SVA Sequence Operators

| Operator | Syntax | Meaning |
|---|---|---|
| Next cycle | `##1` | Exactly 1 cycle later |
| N cycles | `##N` | Exactly N cycles later |
| 0 to N | `##[0:N]` | 0 to N cycles |
| 1 to inf | `##[1:$]` | Eventually (liveness) |
| Throughout | `sig throughout seq` | sig holds during entire seq |
| Within | `s1 within s2` | s1 fully contained in s2 |
| Intersect | `s1 intersect s2` | Both end at same time |
| And | `s1 and s2` | Both hold, end separately |
| Or | `s1 or s2` | At least one holds |
| First match | `first_match(s)` | Stops on first completion |
| Not | `not seq` | Sequence must not occur |

---

## 15.3 SVA Built-in Functions

```systemverilog
$rose(sig)       // sig transitioned from 0 to 1
$fell(sig)       // sig transitioned from 1 to 0
$stable(sig)     // sig has not changed
$past(sig, N)    // value of sig N cycles ago
$countones(expr) // number of 1 bits
$onehot(expr)    // exactly one bit set
$onehot0(expr)   // at most one bit set
$isunknown(expr) // any bit is X or Z
```

---

## 15.4 SVA Property Templates

### Handshake Protocol (VALID/READY)
```systemverilog
default clocking proto_clk @(posedge clk); endclocking
default disable iff (!rst_n);

// VALID must not deassert before READY (AXI rule)
property p_valid_stable;
  valid && !ready |=> valid;
endproperty
P_VALID_STABLE: assert property(p_valid_stable);

// Transfer occurs when both asserted
property p_transfer_on_handshake;
  valid && ready |-> ##1 $past(valid,1) && $past(ready,1);
endproperty

// Request must get response within N cycles
property p_response_latency(max_lat);
  valid && ready |-> ##[1:max_lat] resp_valid;
endproperty
P_LATENCY: assert property(p_response_latency(64));
```

### FSM Invariants
```systemverilog
// One-hot state encoding
property p_state_onehot;
  $onehot(state);
endproperty
P_STATE_ONEHOT: assert property(p_state_onehot);

// No dead states (reachability — use cover)
COV_IDLE:    cover property(state == IDLE);
COV_ACTIVE:  cover property(state == ACTIVE);
COV_DRAIN:   cover property(state == DRAIN);
COV_ERROR:   cover property(state == ERROR);

// No invalid transitions
property p_no_invalid_trans;
  (state == IDLE) |=> (state inside {IDLE, ACTIVE});
endproperty
```

### Data Integrity
```systemverilog
// Write-then-read consistency
property p_write_read_data;
  logic [31:0] wr_data;
  (write_en, wr_data = wdata) |=>
  ##[1:100] (read_en && rdata == wr_data);
endproperty

// Counter monotonicity
property p_counter_monotonic;
  !clear |=> counter >= $past(counter);
endproperty
```

### Liveness
```systemverilog
// Eventual response — no stall forever
property p_no_stall;
  req |-> ##[1:$] ack;
endproperty
P_NO_STALL: assert property(p_no_stall);

// Pipeline eventually drains
property p_pipeline_drains;
  (valid_in && !valid_out) |-> ##[1:PIPE_DEPTH+4] valid_out;
endproperty
```

---

## 15.5 Bind Blocks — Portable Assertion Integration

```systemverilog
// Assertion module — portable, reusable
module axi4_protocol_checker #(
  parameter DATA_WIDTH = 64,
  parameter ID_WIDTH   = 8
)(
  input logic clk, rst_n,
  // AXI write channels
  input logic [ID_WIDTH-1:0] awid,
  input logic [31:0]         awaddr,
  input logic [7:0]          awlen,
  input logic                awvalid, awready,
  input logic                wvalid, wready, wlast,
  input logic [1:0]          bresp,
  input logic                bvalid, bready
);

  default clocking proto_clk @(posedge clk); endclocking
  default disable iff (!rst_n);

  // Insert all protocol SVA properties here
  P_AWVALID_STABLE: assert property(awvalid && !awready |=> awvalid);
  P_WLAST_ONCE:     assert property(wlast |=> !wlast || (wvalid && wready));
  P_BRESP_VALID:    assert property(bvalid |-> bresp inside {2'b00,2'b01,2'b10,2'b11});

endmodule

// Bind to DUT instance — no DUT modification needed
bind dut_top axi4_protocol_checker #(
  .DATA_WIDTH(64),
  .ID_WIDTH(8)
) u_axi4_chk (
  .clk      (clk),
  .rst_n    (rst_n),
  .awid     (axi_if.awid),
  .awaddr   (axi_if.awaddr),
  .awlen    (axi_if.awlen),
  .awvalid  (axi_if.awvalid),
  .awready  (axi_if.awready),
  .wvalid   (axi_if.wvalid),
  .wready   (axi_if.wready),
  .wlast    (axi_if.wlast),
  .bresp    (axi_if.bresp),
  .bvalid   (axi_if.bvalid),
  .bready   (axi_if.bready)
);
```

---

## 15.6 Formal Verification Apps

### Connectivity Check
```
Objective: Prove every input reaches every expected output
Method: Set each input to a unique value; prove it propagates
Use case: NoC routing, address decode, mux trees
Tools: JasperGold Connectivity App, VC Formal
```

### Deadlock Detection
```
Objective: Prove no reachable state from which no progress is possible
Method: Liveness property + unreachability proof
Use case: FIFO-based pipelines, request/grant arbiters, CHI networks
Property: always eventually (req |-> ##[1:$] gnt)
```

### CDC Formal Verification
```
Objective: Prove all clock-domain crossings are safe
Method: Structural CDC analysis + formal proof of synchronizer correctness
Tools: Spyglass CDC, Meridian CDC, JasperGold CDC App
Common violations: missing synchronizer, combinational loop across domains,
                   reconvergence, gray code violation
```

### Regression-Escape Formal
```
Objective: Find bugs that random simulation missed
Method: Bounded model checking (BMC) on specific properties
Use case: Post-silicon escape analysis, pre-signoff formal check
Tools: JasperGold FPV, VC Formal, Questa Formal
```

---

## 15.7 Formal — Assumption Writing Rules

```systemverilog
// Good assumption — constrain input, don't overconstrain
assume property(awlen < 8'h10);             // limit burst length for proof
assume property(awburst != 2'b11);          // reserved encoding never driven

// Bad assumption — eliminates interesting corner cases
assume property(awvalid == 1);              // overconstrained — always valid
assume property(bresp == 2'b00);            // hides error response behavior
```

**Vacuity Check:** Every property must have a cover that its antecedent can be triggered.
A vacuous property (antecedent never triggers) proves trivially and gives false confidence.

```systemverilog
// For every assert property, add a cover:
COV_P_AWVALID_STABLE: cover property(awvalid && !awready);
// If this cover is unreachable, the assert is vacuous.
```

---

## 15.8 Formal Debug Workflow

```
1. Run formal tool → property fails
2. Examine counterexample trace in waveform viewer
3. Identify: is the failure a real bug or a missing assumption?
4. If real bug: document, report to RTL engineer
5. If missing assumption: add assume property + justify why this is valid
6. Re-run proof → should now pass or find new counterexample
7. Check vacuity: does the antecedent ever fire?
8. Check coverage: what percentage of state space is proven?
```

---

## 15.9 SVA QA Checklist

☐ Default clocking block declared
☐ Default disable iff (!rst_n) declared
☐ Antecedent and consequent clearly commented
☐ Every assert has a corresponding cover (vacuity check)
☐ No overlapping temporal operators creating ambiguity
☐ Liveness properties included (not just safety)
☐ Bind blocks used for portability (not inline in DUT)
☐ Formal run confirms all properties pass (not just simulate)
☐ Vacuous properties identified and documented
☐ Disabled assertions reviewed and justified
