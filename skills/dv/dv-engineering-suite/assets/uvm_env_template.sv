// ============================================================
// UVM Environment Skeleton — Top Level
// DV Engineering Bible Vol I — Chapter 14
// Conventions: m_ members, _h handles, config_db throughout
// Replace <DUT_NAME>, <PROTO>, <IF_TYPE> with project values
// ============================================================

// ---- Environment Config Object ----
class dut_env_cfg extends uvm_object;
  `uvm_object_utils(dut_env_cfg)

  // Sub-agent configs — populated by test before build_phase
  rand proto_agent_cfg  m_proto_agent_cfg_h;   // replace with actual protocol config class

  // Global knobs
  bit m_has_scoreboard  = 1;
  bit m_has_coverage    = 1;
  bit m_passive_mode    = 0;   // 1 = no drivers, monitors only

  // Interface handle — set via config_db in test
  virtual dut_if m_vif;        // replace dut_if with your interface type

  function new(string name = "dut_env_cfg");
    super.new(name);
    m_proto_agent_cfg_h = proto_agent_cfg::type_id::create("m_proto_agent_cfg_h");
  endfunction
endclass


// ---- Top-Level Environment ----
class dut_env extends uvm_env;
  `uvm_component_utils(dut_env)

  // Sub-components
  proto_agent        m_proto_agent_h;    // replace with actual agent class
  dut_scoreboard     m_scoreboard_h;
  dut_coverage       m_coverage_h;

  dut_env_cfg        m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);

    // Pull config from config_db — fatal if missing
    if (!uvm_config_db#(dut_env_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "dut_env_cfg not found in config_db")

    // Push sub-agent config down
    uvm_config_db#(proto_agent_cfg)::set(
      this, "m_proto_agent_h*", "m_cfg_h", m_cfg_h.m_proto_agent_cfg_h);

    // Build sub-components
    m_proto_agent_h = proto_agent::type_id::create("m_proto_agent_h", this);

    if (m_cfg_h.m_has_scoreboard)
      m_scoreboard_h = dut_scoreboard::type_id::create("m_scoreboard_h", this);

    if (m_cfg_h.m_has_coverage)
      m_coverage_h = dut_coverage::type_id::create("m_coverage_h", this);
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);

    // Connect monitor analysis port to scoreboard
    if (m_cfg_h.m_has_scoreboard)
      m_proto_agent_h.m_monitor_h.m_ap.connect(m_scoreboard_h.m_analysis_export);

    // Connect monitor analysis port to coverage
    if (m_cfg_h.m_has_coverage)
      m_proto_agent_h.m_monitor_h.m_ap.connect(m_coverage_h.m_analysis_export);
  endfunction

endclass


// ---- UVM Agent Skeleton ----
class proto_agent extends uvm_agent;
  `uvm_component_utils(proto_agent)

  proto_driver     m_driver_h;
  proto_monitor    m_monitor_h;
  proto_sequencer  m_sequencer_h;
  proto_agent_cfg  m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);

    if (!uvm_config_db#(proto_agent_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "proto_agent_cfg not found in config_db")

    // Monitor always built; driver/sequencer only in active mode
    m_monitor_h   = proto_monitor::type_id::create("m_monitor_h", this);
    if (m_cfg_h.m_is_active == UVM_ACTIVE) begin
      m_driver_h    = proto_driver::type_id::create("m_driver_h", this);
      m_sequencer_h = proto_sequencer::type_id::create("m_sequencer_h", this);
    end
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    if (m_cfg_h.m_is_active == UVM_ACTIVE)
      m_driver_h.seq_item_port.connect(m_sequencer_h.seq_item_export);
  endfunction

endclass


// ---- Base Test ----
class dut_base_test extends uvm_test;
  `uvm_component_utils(dut_base_test)

  dut_env       m_env_h;
  dut_env_cfg   m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);

    m_cfg_h = dut_env_cfg::type_id::create("m_cfg_h");

    // Pull virtual interface from top-level config_db
    if (!uvm_config_db#(virtual dut_if)::get(this, "", "m_vif", m_cfg_h.m_vif))
      `uvm_fatal(get_name(), "Virtual interface dut_if not found in config_db")

    // Push env config
    uvm_config_db#(dut_env_cfg)::set(this, "m_env_h*", "m_cfg_h", m_cfg_h);

    m_env_h = dut_env::type_id::create("m_env_h", this);
  endfunction

  task run_phase(uvm_phase phase);
    proto_base_seq m_seq_h = proto_base_seq::type_id::create("m_seq_h");
    phase.raise_objection(this, "base_test run");
    m_seq_h.start(m_env_h.m_proto_agent_h.m_sequencer_h);
    phase.drop_objection(this, "base_test run");
  endtask

endclass
