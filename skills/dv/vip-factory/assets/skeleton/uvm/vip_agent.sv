// =============================================================================
// AVIK VIP FACTORY — Reusable VIP Skeleton
// File: uvm/driver/<vip>_driver.sv
// Item 11: Reusable VIP Skeleton — Driver Layer
// =============================================================================

class <vip>_driver extends uvm_driver#(<vip>_seq_item);
  `uvm_component_utils(<vip>_driver)

  virtual <vip>_if.master_mp m_vif;   // virtual interface handle
  <vip>_agent_cfg             m_cfg_h; // agent config

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(<vip>_agent_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "<vip>_agent_cfg not found in config_db")
    m_vif = m_cfg_h.m_vif;
  endfunction

  task run_phase(uvm_phase phase);
    <vip>_seq_item req, rsp;
    drive_reset();
    forever begin
      seq_item_port.get_next_item(req);
      `uvm_info(get_name(), $sformatf("Driving: %s", req.convert2string()), UVM_HIGH)
      drive_item(req);
      rsp = <vip>_seq_item::type_id::create("rsp");
      rsp.copy(req);
      rsp.set_id_info(req);
      seq_item_port.item_done(rsp);
    end
  endtask

  virtual task drive_reset();
    // Drive all outputs to safe reset values
    @(posedge m_vif.clk);
    // TODO: implement protocol-specific reset driving
    `uvm_info(get_name(), "Reset sequence complete", UVM_MEDIUM)
  endtask

  virtual task drive_item(<vip>_seq_item item);
    // Delay cycles
    repeat(item.m_delay) @(posedge m_vif.clk);
    // TODO: implement protocol-specific transaction driving
    // Example for a simple bus:
    // @(posedge m_vif.clk);
    // m_vif.addr  <= item.m_addr;
    // m_vif.wdata <= item.m_data;
    // m_vif.write <= item.m_write;
    // m_vif.valid <= 1;
    // @(posedge m_vif.clk iff m_vif.ready);
    // m_vif.valid <= 0;
  endtask

endclass : <vip>_driver

// =============================================================================
// File: uvm/monitor/<vip>_monitor.sv
// Item 11: Reusable VIP Skeleton — Monitor Layer
// =============================================================================

class <vip>_monitor extends uvm_monitor;
  `uvm_component_utils(<vip>_monitor)

  virtual <vip>_if.monitor_mp    m_vif;
  <vip>_agent_cfg                m_cfg_h;
  uvm_analysis_port#(<vip>_seq_item) m_ap;  // broadcasts to SB + coverage

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    m_ap = new("m_ap", this);
    if (!uvm_config_db#(<vip>_agent_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "<vip>_agent_cfg not found in config_db")
    m_vif = m_cfg_h.m_vif;
  endfunction

  task run_phase(uvm_phase phase);
    <vip>_seq_item t;
    forever begin
      collect_transaction(t);
      `uvm_info(get_name(), $sformatf("Observed: %s", t.convert2string()), UVM_HIGH)
      m_ap.write(t);
    end
  endtask

  virtual task collect_transaction(output <vip>_seq_item t);
    t = <vip>_seq_item::type_id::create("observed");
    // TODO: implement protocol-specific bus observation
    // Example:
    // @(posedge m_vif.clk iff (m_vif.valid && m_vif.ready));
    // t.m_addr  = m_vif.addr;
    // t.m_write = m_vif.write;
    // if (m_vif.write) t.m_data  = m_vif.wdata;
    // else             t.m_rdata = m_vif.rdata;
  endtask

endclass : <vip>_monitor

// =============================================================================
// File: uvm/agent/<vip>_agent.sv
// Item 11: Reusable VIP Skeleton — Agent
// =============================================================================

class <vip>_agent extends uvm_agent;
  `uvm_component_utils(<vip>_agent)

  <vip>_driver     m_driver_h;
  <vip>_monitor    m_monitor_h;
  <vip>_sequencer  m_sequencer_h;
  <vip>_agent_cfg  m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);
    if (!uvm_config_db#(<vip>_agent_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "<vip>_agent_cfg not found in config_db")

    // Monitor always built — active and passive modes
    m_monitor_h = <vip>_monitor::type_id::create("m_monitor_h", this);

    // Driver + sequencer only in active mode
    if (m_cfg_h.m_is_active == UVM_ACTIVE) begin
      m_driver_h    = <vip>_driver::type_id::create("m_driver_h", this);
      m_sequencer_h = <vip>_sequencer::type_id::create("m_sequencer_h", this);
    end
  endfunction

  function void connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    if (m_cfg_h.m_is_active == UVM_ACTIVE)
      m_driver_h.seq_item_port.connect(m_sequencer_h.seq_item_export);
  endfunction

endclass : <vip>_agent

// =============================================================================
// File: uvm/agent/<vip>_agent_cfg.sv
// Item 11: Reusable VIP Skeleton — Agent Config Object
// =============================================================================

class <vip>_agent_cfg extends uvm_object;
  `uvm_object_utils(<vip>_agent_cfg)

  // Interface handle — set from test via config_db
  virtual <vip>_if          m_vif;

  // Active or passive mode
  uvm_active_passive_enum   m_is_active        = UVM_ACTIVE;

  // Feature enables
  bit                       m_has_coverage     = 1;
  bit                       m_has_checks       = 1;

  // Protocol config knobs (customize per VIP)
  int unsigned              m_max_outstanding  = 16;
  int unsigned              m_response_timeout = 1000; // cycles

  function new(string name = "<vip>_agent_cfg");
    super.new(name);
  endfunction

endclass : <vip>_agent_cfg
