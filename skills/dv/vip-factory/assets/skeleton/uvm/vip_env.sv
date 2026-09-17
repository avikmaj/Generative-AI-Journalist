// =============================================================================
// AVIK VIP FACTORY — Reusable VIP Skeleton
// File: uvm/env/<vip>_env.sv
// Item 11: Reusable VIP Skeleton — Environment
// =============================================================================

class <vip>_env extends uvm_env;
  `uvm_component_utils(<vip>_env)

  <vip>_agent        m_agent_h[];
  <vip>_scoreboard   m_scoreboard_h;
  <vip>_coverage     m_coverage_h;
  <vip>_env_cfg      m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(<vip>_env_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "<vip>_env_cfg not found in config_db")

    // Build agents
    m_agent_h = new[m_cfg_h.m_num_agents];
    foreach (m_agent_h[i]) begin
      uvm_config_db#(<vip>_agent_cfg)::set(
        this, $sformatf("m_agent_h[%0d]*", i),
        "m_cfg_h", m_cfg_h.m_agent_cfg_h[i]);
      m_agent_h[i] = <vip>_agent::type_id::create(
        $sformatf("m_agent_h[%0d]", i), this);
    end

    // Build scoreboard and coverage
    if (m_cfg_h.m_has_scoreboard)
      m_scoreboard_h = <vip>_scoreboard::type_id::create("m_scoreboard_h", this);
    if (m_cfg_h.m_has_coverage)
      m_coverage_h   = <vip>_coverage::type_id::create("m_coverage_h", this);
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    foreach (m_agent_h[i]) begin
      if (m_cfg_h.m_has_scoreboard)
        m_agent_h[i].m_monitor_h.m_ap.connect(m_scoreboard_h.m_analysis_export);
      if (m_cfg_h.m_has_coverage)
        m_agent_h[i].m_monitor_h.m_ap.connect(m_coverage_h.m_analysis_export);
    end
  endfunction

endclass : <vip>_env

// =============================================================================
// File: uvm/env/<vip>_env_cfg.sv
// =============================================================================

class <vip>_env_cfg extends uvm_object;
  `uvm_object_utils(<vip>_env_cfg)

  <vip>_agent_cfg   m_agent_cfg_h[];
  int unsigned      m_num_agents    = 1;
  bit               m_has_scoreboard = 1;
  bit               m_has_coverage   = 1;

  function new(string name = "<vip>_env_cfg");
    super.new(name);
  endfunction

  function void build();
    m_agent_cfg_h = new[m_num_agents];
    foreach (m_agent_cfg_h[i])
      m_agent_cfg_h[i] = <vip>_agent_cfg::type_id::create(
        $sformatf("m_agent_cfg_h[%0d]", i));
  endfunction

endclass : <vip>_env_cfg

// =============================================================================
// File: uvm/scoreboard/<vip>_scoreboard.sv
// Item 11: Reusable VIP Skeleton — Scoreboard (In-Order)
// =============================================================================

`uvm_analysis_imp_decl(_stim)
`uvm_analysis_imp_decl(_resp)

class <vip>_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(<vip>_scoreboard)

  uvm_analysis_imp_stim#(<vip>_seq_item, <vip>_scoreboard) m_stim_export;
  uvm_analysis_imp_resp#(<vip>_seq_item, <vip>_scoreboard) m_analysis_export;

  <vip>_seq_item  m_expected_q[$];
  int unsigned    m_match_count = 0;
  int unsigned    m_error_count = 0;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    m_stim_export    = new("m_stim_export",    this);
    m_analysis_export = new("m_analysis_export", this);
  endfunction

  // Called when monitor observes a stimulus transaction
  function void write_stim(<vip>_seq_item t);
    <vip>_seq_item exp = <vip>_seq_item::type_id::create("exp");
    predict(t, exp);
    m_expected_q.push_back(exp);
    `uvm_info(get_name(), $sformatf("Expected queued: %s", exp.convert2string()), UVM_HIGH)
  endfunction

  // Called when monitor observes a response transaction
  function void write_resp(<vip>_seq_item t);
    <vip>_seq_item exp;
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
      `uvm_info(get_name(), $sformatf(
        "MATCH [%0d]: %s", m_match_count, t.convert2string()), UVM_HIGH)
    end
  endfunction

  // Prediction function — implement DUT functional model here
  virtual function void predict(<vip>_seq_item stim, ref <vip>_seq_item exp);
    // TODO: compute expected response from stimulus
    // For a read: exp.m_rdata = memory_model[stim.m_addr]
    // For a write: memory_model[stim.m_addr] = stim.m_data; exp.m_resp = OKAY
    exp.m_resp = 2'b00;  // placeholder: OKAY response
  endfunction

  function void check_phase(uvm_phase phase);
    if (m_expected_q.size() != 0)
      `uvm_error(get_name(), $sformatf(
        "%0d expected responses never received", m_expected_q.size()))
    `uvm_info(get_name(), $sformatf(
      "Scoreboard: %0d matches, %0d errors", m_match_count, m_error_count), UVM_NONE)
  endfunction

endclass : <vip>_scoreboard

// =============================================================================
// File: uvm/coverage/<vip>_coverage.sv
// Item 11: Reusable VIP Skeleton — Coverage Collector
// =============================================================================

class <vip>_coverage extends uvm_subscriber#(<vip>_seq_item);
  `uvm_component_utils(<vip>_coverage)

  // Sampled transaction fields
  <vip>_seq_item m_t;

  // ── Covergroups ────────────────────────────────────────────────────────────
  covergroup <vip>_txn_cg;
    option.per_instance = 1;
    option.comment      = "<VIP> Transaction Coverage";

    cp_txn_type: coverpoint m_t.m_txn_type {
      bins WRITE = {<vip>_seq_item::TXN_WRITE};
      bins READ  = {<vip>_seq_item::TXN_READ};
      bins IDLE  = {<vip>_seq_item::TXN_IDLE};
    }

    cp_addr_region: coverpoint m_t.m_addr[31:28] {
      bins region[] = {[0:15]};   // all 16 address regions
    }

    cp_delay: coverpoint m_t.m_delay {
      bins no_delay    = {0};
      bins short_delay = {[1:4]};
      bins long_delay  = {[5:$]};
    }

    cx_type_region: cross cp_txn_type, cp_addr_region;
  endgroup

  // ── Constructor ────────────────────────────────────────────────────────────
  function new(string name, uvm_component parent);
    super.new(name, parent);
    <vip>_txn_cg = new();
  endfunction

  // Called by analysis port on every observed transaction
  function void write(<vip>_seq_item t);
    m_t = t;
    <vip>_txn_cg.sample();
  endfunction

endclass : <vip>_coverage

// =============================================================================
// File: uvm/assertions/<vip>_assertions.sv
// Item 11: Reusable VIP Skeleton — Protocol Assertions (bind block)
// =============================================================================

module <vip>_protocol_checker (
  input logic clk,
  input logic rst_n
  // TODO: add protocol-specific signals
  // input logic valid, ready, ...
);

  default clocking proto_clk @(posedge clk); endclocking
  default disable iff (!rst_n);

  // ── Protocol invariants — customize per protocol ───────────────────────────

  // Example: VALID must not deassert without READY
  // property p_valid_stable;
  //   valid && !ready |=> valid;
  // endproperty
  // P_VALID_STABLE: assert property(p_valid_stable)
  //   else `uvm_error("SVA", "VALID deasserted without READY");
  // COV_VALID_STABLE: cover property(valid && !ready);

  // Example: Response within max latency
  // property p_response_latency;
  //   req_valid && req_ready |-> ##[1:256] rsp_valid;
  // endproperty
  // P_RSP_LATENCY: assert property(p_response_latency);
  // COV_RSP_LATENCY: cover property(req_valid && req_ready);

endmodule : <vip>_protocol_checker

// Bind to DUT — no DUT modification required
// bind <dut_top> <vip>_protocol_checker u_checker (
//   .clk   (clk),
//   .rst_n (rst_n)
//   // map DUT signals here
// );
