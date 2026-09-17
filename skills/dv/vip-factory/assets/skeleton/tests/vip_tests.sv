// =============================================================================
// AVIK VIP FACTORY — Reusable Test Templates
// Item 12: Reusable test/sequence templates
// Copy for each new VIP — search/replace <vip> with protocol name
// =============================================================================

// =============================================================================
// BASE TEST — parent for all VIP tests
// =============================================================================

class <vip>_base_test extends uvm_test;
  `uvm_component_utils(<vip>_base_test)

  <vip>_env      m_env_h;
  <vip>_env_cfg  m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    m_cfg_h = <vip>_env_cfg::type_id::create("m_cfg_h");
    m_cfg_h.build();

    // Pull virtual interface from config_db (set in tb_top)
    if (!uvm_config_db#(virtual <vip>_if)::get(
        this, "", "m_vif", m_cfg_h.m_agent_cfg_h[0].m_vif))
      `uvm_fatal(get_name(), "Virtual interface <vip>_if not found in config_db")

    uvm_config_db#(<vip>_env_cfg)::set(this, "m_env_h*", "m_cfg_h", m_cfg_h);
    m_env_h = <vip>_env::type_id::create("m_env_h", this);
  endfunction

  // Base run_phase — override in derived tests
  task run_phase(uvm_phase phase);
    <vip>_base_seq m_seq_h = <vip>_base_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "base_test running");
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "base_test done");
  endtask

endclass : <vip>_base_test

// =============================================================================
// SMOKE TEST — L1: basic functionality, fixed seeds only
// =============================================================================

class <vip>_smoke_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_smoke_test)

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  task run_phase(uvm_phase phase);
    <vip>_write_seq  m_wr_seq;
    <vip>_read_seq   m_rd_seq;

    phase.raise_objection(this, "smoke_test running");

    // Basic write
    m_wr_seq = <vip>_write_seq::type_id::create("m_wr_seq");
    m_wr_seq.m_num_transactions = 1;
    m_wr_seq.start(m_env_h.m_agent_h[0].m_sequencer_h);

    // Basic read
    m_rd_seq = <vip>_read_seq::type_id::create("m_rd_seq");
    m_rd_seq.m_num_transactions = 1;
    m_rd_seq.start(m_env_h.m_agent_h[0].m_sequencer_h);

    `uvm_info(get_name(), "Smoke test complete", UVM_NONE)
    phase.drop_objection(this, "smoke_test done");
  endtask

endclass : <vip>_smoke_test

// =============================================================================
// WRITE TEST — L2: directed write channel
// =============================================================================

class <vip>_write_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_write_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_write_seq m_seq_h = <vip>_write_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "write_test");
    m_seq_h.m_num_transactions = 20;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "write_test done");
  endtask
endclass

// =============================================================================
// READ TEST — L2: directed read channel
// =============================================================================

class <vip>_read_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_read_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_read_seq m_seq_h = <vip>_read_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "read_test");
    m_seq_h.m_num_transactions = 20;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "read_test done");
  endtask
endclass

// =============================================================================
// RANDOM TEST — L3: constrained-random, coverage-driven
// =============================================================================

class <vip>_random_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_random_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_random_seq m_seq_h = <vip>_random_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "random_test");
    m_seq_h.m_num_transactions = 200;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "random_test done");
  endtask
endclass

// =============================================================================
// ERROR TEST — Negative test: expected violations must be DETECTED
// PASS = EXPECTED_FAILURE_DETECTED  (not PASS in normal sense)
// =============================================================================

class <vip>_error_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_error_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_error_seq m_seq_h = <vip>_error_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "error_test");
    `uvm_info(get_name(),
      "NEGATIVE TEST: expected protocol violation — PASS = violation DETECTED",
      UVM_NONE)
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "error_test done");
  endtask
endclass

// =============================================================================
// STRESS TEST — L4: maximum load, long duration
// =============================================================================

class <vip>_stress_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_stress_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_random_seq m_seq_h = <vip>_random_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "stress_test");
    m_seq_h.m_num_transactions = 10_000;  // high count for stress
    m_seq_h.m_max_outstanding  = 16;      // maximum outstanding
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "stress_test done");
  endtask
endclass

// =============================================================================
// BACKPRESSURE TEST — L2: READY deassert scenarios
// =============================================================================

class <vip>_backpressure_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_backpressure_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_random_seq m_seq_h = <vip>_random_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "backpressure_test");
    // Enable backpressure in agent config
    m_cfg_h.m_agent_cfg_h[0].m_has_backpressure = 1;
    m_seq_h.m_num_transactions = 100;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);
    phase.drop_objection(this, "backpressure_test done");
  endtask
endclass

// =============================================================================
// RESET TEST — L2: mid-transaction reset
// =============================================================================

class <vip>_reset_test extends <vip>_base_test;
  `uvm_component_utils(<vip>_reset_test)
  function new(string name, uvm_component parent); super.new(name, parent); endfunction

  task run_phase(uvm_phase phase);
    <vip>_random_seq m_seq_h;
    phase.raise_objection(this, "reset_test");

    // Send some traffic
    m_seq_h = <vip>_random_seq::type_id::create("pre_reset_seq");
    m_seq_h.m_num_transactions = 10;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);

    // Assert reset mid-transaction
    `uvm_info(get_name(), "Asserting mid-transaction reset", UVM_NONE)
    // TODO: drive reset via TB interface or reset sequence

    // Send traffic after reset — must work correctly
    m_seq_h = <vip>_random_seq::type_id::create("post_reset_seq");
    m_seq_h.m_num_transactions = 20;
    m_seq_h.start(m_env_h.m_agent_h[0].m_sequencer_h);

    phase.drop_objection(this, "reset_test done");
  endtask
endclass
