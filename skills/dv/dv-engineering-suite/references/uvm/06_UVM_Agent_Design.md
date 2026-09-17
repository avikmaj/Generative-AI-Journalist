# Module 06 — UVM Agent Design
## Driver · Monitor · Sequencer · Agent Config · Passive/Active

---

## 6.1 Agent Config Object

```systemverilog
class proto_agent_cfg extends uvm_object;
  `uvm_object_utils(proto_agent_cfg)
  virtual proto_if   m_vif;
  uvm_active_passive_enum m_is_active = UVM_ACTIVE;
  bit m_has_coverage   = 1;
  bit m_protocol_check = 1;
  int m_agent_id       = 0;
  function new(string name = "proto_agent_cfg"); super.new(name); endfunction
endclass
```

## 6.2 Driver Pattern

```systemverilog
class proto_driver extends uvm_driver#(proto_seq_item);
  `uvm_component_utils(proto_driver)
  virtual proto_if.master m_vif;
  proto_agent_cfg         m_cfg_h;

  task run_phase(uvm_phase phase);
    proto_seq_item req, rsp;
    forever begin
      seq_item_port.get_next_item(req);
      drive_transaction(req);         // drive DUT
      rsp = proto_seq_item::type_id::create("rsp");
      rsp.copy(req);
      rsp.set_id_info(req);
      seq_item_port.item_done(rsp);   // return response
    end
  endtask

  virtual task drive_transaction(proto_seq_item item);
    @(m_vif.master_cb);
    m_vif.master_cb.awvalid <= 1;
    m_vif.master_cb.awaddr  <= item.awaddr;
    m_vif.master_cb.awlen   <= item.awlen;
    @(posedge m_vif.clk iff m_vif.awready);
    m_vif.master_cb.awvalid <= 0;
  endtask
endclass
```

## 6.3 Monitor Pattern

```systemverilog
class proto_monitor extends uvm_monitor;
  `uvm_component_utils(proto_monitor)
  virtual proto_if.slave m_vif;
  uvm_analysis_port#(proto_seq_item) m_ap;

  function void build_phase(uvm_phase phase);
    m_ap = new("m_ap", this);
  endfunction

  task run_phase(uvm_phase phase);
    proto_seq_item t;
    forever begin
      collect_transaction(t);
      m_ap.write(t);           // broadcast to scoreboard + coverage
    end
  endtask

  virtual task collect_transaction(output proto_seq_item t);
    t = proto_seq_item::type_id::create("t");
    @(posedge m_vif.clk iff (m_vif.awvalid && m_vif.awready));
    t.awaddr  = m_vif.awaddr;
    t.awlen   = m_vif.awlen;
    t.awburst = m_vif.awburst;
  endtask
endclass
```

## 6.4 Active vs Passive

| Mode | Components built | Use case |
|---|---|---|
| UVM_ACTIVE | Driver + Monitor + Sequencer | DUT stimulus + observation |
| UVM_PASSIVE | Monitor only | Protocol checking without driving |

```systemverilog
// In agent build_phase — conditionally build active components
if (m_cfg_h.m_is_active == UVM_ACTIVE) begin
  m_driver_h    = proto_driver::type_id::create("m_driver_h", this);
  m_sequencer_h = proto_sequencer::type_id::create("m_sequencer_h", this);
end
// Monitor always built regardless of active/passive
m_monitor_h = proto_monitor::type_id::create("m_monitor_h", this);
```
