# Module 22 — Templates and Assets
## Fill-in Scaffolds for Every Deliverable

---

## T01 — Vplan Feature Entry

```yaml
# Copy-paste for each feature extracted from spec
- id: F###
  name: <Feature_Name>
  priority: P0               # P0=critical / P1=functional / P2=edge
  spec_ref: Sec X.Y, p.NNN
  risk: HIGH                 # HIGH|MEDIUM|LOW
  methodology: constrained_random  # or directed / formal / hybrid
  estimated_tests: 100
  dependencies: []           # [F001, F002]

  scenarios:
    - id: F###_S01
      name: <Scenario_Name>
      stimulus: constrained_random
      priority: P0
      coverage:
        - covergroup: <cg_name>
          coverpoint: <cp_name>
          bins: [bin1, bin2]
      assertions: [p_<property_name>]
      expected_bug_density: medium   # low|medium|high
      notes: ""
```

---

## T02 — UVM Sequence (Constrained-Random)

```systemverilog
class <name>_seq extends <base>_seq;
  `uvm_object_utils(<name>_seq)

  // Coverage target: <covergroup>.<coverpoint> — <bin>

  // Configurable knobs
  int unsigned m_num_transactions = 10;
  bit          m_enable_backpressure = 0;

  function new(string name = "<name>_seq");
    super.new(name);
  endfunction

  task body();
    <proto>_seq_item req;
    repeat(m_num_transactions) begin
      req = <proto>_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize() with {
        // Add constraint block here
        // Example: awburst == 2'b10; awlen == 8'hFF;
      }) `uvm_fatal(get_name(), "Randomization failed")
      finish_item(req);
    end
  endtask
endclass
```

---

## T03 — UVM Agent

```systemverilog
class <proto>_agent extends uvm_agent;
  `uvm_component_utils(<proto>_agent)

  <proto>_driver     m_driver_h;
  <proto>_monitor    m_monitor_h;
  <proto>_sequencer  m_sequencer_h;
  <proto>_agent_cfg  m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(<proto>_agent_cfg)::get(
        this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "<proto>_agent_cfg not found in config_db")

    m_monitor_h = <proto>_monitor::type_id::create("m_monitor_h", this);
    if (m_cfg_h.m_is_active == UVM_ACTIVE) begin
      m_driver_h    = <proto>_driver::type_id::create("m_driver_h", this);
      m_sequencer_h = <proto>_sequencer::type_id::create("m_sequencer_h", this);
    end
  endfunction

  function void connect_phase(uvm_phase phase);
    if (m_cfg_h.m_is_active == UVM_ACTIVE)
      m_driver_h.seq_item_port.connect(m_sequencer_h.seq_item_export);
  endfunction
endclass
```

---

## T04 — Scoreboard (In-Order)

```systemverilog
`uvm_analysis_imp_decl(_master)
`uvm_analysis_imp_decl(_slave)

class <dut>_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(<dut>_scoreboard)

  uvm_analysis_imp_master#(<proto>_seq_item, <dut>_scoreboard) m_master_export;
  uvm_analysis_imp_slave #(<proto>_seq_item, <dut>_scoreboard) m_slave_export;

  <proto>_seq_item m_expected_q[$];
  int unsigned m_match_count  = 0;
  int unsigned m_error_count  = 0;

  function void build_phase(uvm_phase phase);
    m_master_export = new("m_master_export", this);
    m_slave_export  = new("m_slave_export",  this);
  endfunction

  // Called when master monitor observes a transaction
  function void write_master(<proto>_seq_item t);
    <proto>_seq_item exp = <proto>_seq_item::type_id::create("exp");
    // Build expected response from stimulus
    // exp.data = predict(t);
    m_expected_q.push_back(exp);
    `uvm_info(get_name(), $sformatf("Expected queued: %s", exp.convert2string()), UVM_HIGH)
  endfunction

  // Called when slave monitor observes a response
  function void write_slave(<proto>_seq_item t);
    <proto>_seq_item exp;
    if (m_expected_q.size() == 0) begin
      `uvm_error(get_name(), $sformatf(
        "UNEXPECTED RESPONSE: %s — expected queue empty", t.convert2string()))
      m_error_count++;
      return;
    end
    exp = m_expected_q.pop_front();
    if (!t.compare(exp)) begin
      `uvm_error(get_name(), $sformatf(
        "MISMATCH:\n  Expected: %s\n  Actual:   %s",
        exp.convert2string(), t.convert2string()))
      m_error_count++;
    end else begin
      m_match_count++;
      `uvm_info(get_name(), $sformatf("MATCH [%0d]: %s", m_match_count, t.convert2string()), UVM_HIGH)
    end
  endfunction

  function void check_phase(uvm_phase phase);
    if (m_expected_q.size() != 0)
      `uvm_error(get_name(), $sformatf(
        "%0d expected responses never received", m_expected_q.size()))
    `uvm_info(get_name(), $sformatf(
      "Scoreboard summary: %0d matches, %0d errors",
      m_match_count, m_error_count), UVM_NONE)
  endfunction
endclass
```

---

## T05 — Covergroup

```systemverilog
covergroup <name>_cg @(posedge clk iff (<sampling_condition>));
  option.per_instance = 1;
  option.comment      = "<description>";
  option.goal         = 100;

  // Coverpoint 1
  cp_<field1>: coverpoint <signal1> {
    bins val_A = {<val>};
    bins val_B = {[<lo>:<hi>]};
    bins others = default;
  }

  // Coverpoint 2
  cp_<field2>: coverpoint <signal2> {
    bins state_IDLE   = {STATE_IDLE};
    bins state_ACTIVE = {STATE_ACTIVE};
    bins state_ERROR  = {STATE_ERROR};
  }

  // Cross coverage
  cx_<f1>_<f2>: cross cp_<field1>, cp_<field2> {
    // Optional: exclude impossible combinations
    illegal_bins impossible = binsof(cp_<field1>.val_A) && binsof(cp_<field2>.state_ERROR);
  }
endgroup
```

---

## T06 — SVA Property Set

```systemverilog
// ─── Default Clocking ─────────────────────────────────────
default clocking <proto>_clk @(posedge clk); endclocking
default disable iff (!rst_n);

// ─── Handshake Properties ─────────────────────────────────
// VALID must not deassert without transfer
property p_valid_stable;
  valid && !ready |=> valid;
endproperty
P_VALID_STABLE: assert property(p_valid_stable)
  else `uvm_error("SVA", "VALID deasserted without READY — protocol violation");

// ─── Response Latency ─────────────────────────────────────
property p_response_within_N(max_cyc);
  req_valid && req_ready |-> ##[1:max_cyc] rsp_valid;
endproperty
P_RSP_LATENCY: assert property(p_response_within_N(64));

// ─── Vacuity Cover (one per assert) ───────────────────────
COV_VALID_STABLE: cover property(valid && !ready);
COV_RSP_LATENCY:  cover property(req_valid && req_ready);

// ─── Liveness ─────────────────────────────────────────────
property p_no_deadlock;
  req |-> ##[1:$] ack;
endproperty
P_NO_DEADLOCK: assert property(p_no_deadlock);

// ─── Data Integrity ───────────────────────────────────────
property p_data_stable_during_valid;
  valid && !ready |=> $stable(data);
endproperty
P_DATA_STABLE: assert property(p_data_stable_during_valid);
```

---

## T07 — Debug Triage Report

```yaml
debug_report:
  test: <test_name>
  seed: <seed>
  timestamp: <ISO-8601>
  simulator: VCS S-2021.09-SP1

  failure:
    error_message: "<exact UVM_ERROR/FATAL text>"
    timestamp_ns: <sim time>
    location: "<file>:<line>"

  classification: TB           # TB | DUT | Infra | Flaky
  confidence: 0.85

  root_causes:
    - rank: 1
      hypothesis: "<description>"
      probability: 0.65
      evidence: "<what was observed>"
      grep_command: "grep -A20 '<pattern>' sim.log"

    - rank: 2
      hypothesis: "<description>"
      probability: 0.25
      evidence: "<what would confirm this>"

  waveform:
    signals: [<signal_list>]
    time_window: "<start_ns> to <end_ns>"
    observations: "<what was seen>"

  root_cause_confirmed: false
  fix: ""
  regression_guard: ""       # SVA property or coverage point added
  bug_id: ""
```

---

## T08 — Signoff Evidence Package (Quick Reference)

```
ITEM                          TARGET      STATUS
─────────────────────────────────────────────────
RTM — requirements traced     100%        ______
Functional coverage           ≥95%        ______
Code — statement              ≥90%        ______
Code — branch                 ≥85%        ______
Toggle                        ≥75%        ______
Assertion — exercised         ≥95%        ______
Assertion — vacuous reviewed  All         ______
Assertion — disabled reviewed All         ______
Regression pass rate          ≥99%        ______
Flaky rate                    <1%         ______
Consecutive stable runs       ≥5          ______
P0 bugs open                  0           ______
P1 bugs dispositioned         All         ______
Performance targets met       Per spec    ______
Risk register reviewed        Complete    ______
Waivers approved              All         ______
Review board quorum           Met         ______
Board decision                Approved    ______
```
