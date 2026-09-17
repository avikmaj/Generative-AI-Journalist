# Module 05 — UVM Architecture
## Factory · Phases · Config DB · TLM · Objections · Complete Reference

---

## 5.1 UVM Architecture Overview

```
uvm_test
    └── uvm_env
            ├── uvm_agent (active)
            │       ├── uvm_driver
            │       ├── uvm_monitor
            │       └── uvm_sequencer
            ├── uvm_agent (passive — monitor only)
            ├── uvm_scoreboard
            ├── uvm_coverage_collector
            ├── uvm_virtual_sequencer
            └── uvm_reg_block (RAL)
```

---

## 5.2 UVM Factory

The factory enables component/object replacement without modifying the TB.

```systemverilog
// Registration — every class
class my_driver extends uvm_driver#(my_item);
  `uvm_component_utils(my_driver)
  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction
endclass

// Type override — replace everywhere
my_driver::type_id::set_type_override(
  my_driver_err_inject::get_type());

// Instance override — replace specific instance
my_driver::type_id::set_inst_override(
  my_driver_err_inject::get_type(),
  "uvm_test_top.env.agent.driver");

// Creation — always through factory
my_driver m_driver_h = my_driver::type_id::create("m_driver_h", this);
```

**Rule:** NEVER use `new()` directly for any UVM component or object that may be overridden.

---

## 5.3 UVM Phases — Complete Reference

### Build Phases (top-down execution)
```
build_phase        — create child components; get config; create objects
connect_phase      — connect TLM ports; set sequencer handles
end_of_elaboration — check connectivity; print topology
start_of_simulation — print topology; initialize state
```

### Run Phase (parallel execution)
```
run_phase          — primary simulation phase; raise/drop objections here
  ├── pre_reset_phase
  ├── reset_phase        — drive reset
  ├── post_reset_phase
  ├── pre_configure_phase
  ├── configure_phase    — program DUT registers
  ├── post_configure_phase
  ├── pre_main_phase
  ├── main_phase         — primary test stimulus
  ├── post_main_phase
  ├── pre_shutdown_phase
  ├── shutdown_phase     — drain in-flight transactions
  └── post_shutdown_phase
```

### Cleanup Phases (bottom-up execution)
```
extract_phase      — extract results from components
check_phase        — perform final checks; report errors
report_phase       — generate reports
final_phase        — last opportunity before exit
```

### Phase Objection Pattern
```systemverilog
task run_phase(uvm_phase phase);
  my_seq m_seq_h = my_seq::type_id::create("m_seq_h");
  phase.raise_objection(this, "starting stimulus");
  m_seq_h.start(m_env_h.m_agent_h.m_sequencer_h);
  #100ns; // drain time for in-flight transactions
  phase.drop_objection(this, "stimulus complete");
endtask
```

**Common mistakes:**
- Raising objection after sequence starts → race condition
- Not dropping objection → PH_TIMEOUT
- Dropping too early → DUT response not captured

---

## 5.4 UVM Config DB — Complete Reference

### Set (from higher-level component)
```systemverilog
// Set virtual interface (from top-level module or test)
uvm_config_db#(virtual my_if)::set(
  null,                    // context: null from top module
  "uvm_test_top.*",        // path: wildcard to all children
  "m_vif",                 // field name
  my_if_inst);             // value

// Set from test (preferred)
uvm_config_db#(virtual my_if)::set(
  this,                    // context: the test
  "m_env_h.m_agent_h*",   // path
  "m_vif",
  m_cfg_h.m_vif);

// Set config object
uvm_config_db#(my_env_cfg)::set(
  this, "m_env_h*", "m_cfg_h", m_cfg_h);
```

### Get (in receiving component)
```systemverilog
function void build_phase(uvm_phase phase);
  // Virtual interface — fatal if missing
  if (!uvm_config_db#(virtual my_if)::get(
      this, "", "m_vif", m_vif))
    `uvm_fatal(get_name(), "Virtual interface my_if not in config_db")

  // Config object — fatal if missing
  if (!uvm_config_db#(my_agent_cfg)::get(
      this, "", "m_cfg_h", m_cfg_h))
    `uvm_fatal(get_name(), "my_agent_cfg not in config_db")
endfunction
```

**Rules:**
- ALWAYS `uvm_fatal` on failed get — never silently continue with null
- Use wildcards on set (`*`), empty string on get (`""`)
- Set before the receiving component's `build_phase` runs
- Never pass interface handles through constructor arguments

---

## 5.5 TLM — Transaction Level Modeling

### Port Types

| Port Type | Direction | Use |
|---|---|---|
| `uvm_analysis_port` | Output (broadcast) | Monitor → multiple subscribers |
| `uvm_analysis_export` | Input (FIFO-based) | Receive and buffer |
| `uvm_analysis_imp` | Input (direct call) | Direct `write()` call |
| `uvm_blocking_put_port` | Output (blocking) | Producer → consumer |
| `uvm_blocking_get_port` | Input (blocking) | Pull from producer |
| `uvm_seq_item_pull_port` | Sequencer→Driver | Standard seq/drv connection |

### Analysis Connection Pattern
```systemverilog
// In monitor
uvm_analysis_port#(my_item) m_ap;

// In scoreboard
uvm_analysis_imp#(my_item, my_scoreboard) m_analysis_export;
function void write(my_item t);
  // process transaction
endfunction

// In env connect_phase
m_monitor_h.m_ap.connect(m_scoreboard_h.m_analysis_export);

// One-to-many: use analysis FIFO
uvm_tlm_analysis_fifo#(my_item) m_fifo;
m_monitor_h.m_ap.connect(m_fifo.analysis_export);
// Consumer pulls from: m_fifo.get_export
```

### Multiple Imps (different channels)
```systemverilog
`uvm_analysis_imp_decl(_master)
`uvm_analysis_imp_decl(_slave)

class my_scoreboard extends uvm_scoreboard;
  uvm_analysis_imp_master#(my_item, my_scoreboard) m_master_export;
  uvm_analysis_imp_slave#(my_item,  my_scoreboard) m_slave_export;

  function void write_master(my_item t); ... endfunction
  function void write_slave(my_item t);  ... endfunction
endclass
```

---

## 5.6 UVM Reporting System

```systemverilog
`uvm_info(get_name(),    "Informational message",          UVM_MEDIUM)
`uvm_warning(get_name(), "Warning — may indicate issue",   UVM_NONE)
`uvm_error(get_name(),   "Non-fatal error — test continues", UVM_NONE)
`uvm_fatal(get_name(),   "Fatal — simulation stops immediately", UVM_NONE)

// Verbosity levels
UVM_NONE    = 0    // Always printed
UVM_LOW     = 100  // Important
UVM_MEDIUM  = 200  // Normal (default)
UVM_HIGH    = 400  // Verbose debug
UVM_FULL    = 500  // Maximum debug
```

### Runtime Verbosity Control
```
+UVM_VERBOSITY=UVM_MEDIUM    # default
+UVM_VERBOSITY=UVM_HIGH      # debug sessions
+uvm_set_verbosity=uvm_test_top.env.agent,UVM_HIGH,time,100  # per-component
```

---

## 5.7 UVM Environment Config Object Pattern

```systemverilog
class dut_env_cfg extends uvm_object;
  `uvm_object_utils(dut_env_cfg)

  // Sub-configs
  rand master_agent_cfg m_master_cfg_h[];
  rand slave_agent_cfg  m_slave_cfg_h[];

  // Global knobs
  bit     m_has_scoreboard = 1;
  bit     m_has_coverage   = 1;
  int     m_num_masters    = 1;
  int     m_num_slaves     = 1;

  // Interface handles (set from test via config_db)
  virtual dut_if m_vif;

  // Constraints
  constraint c_valid_config {
    m_num_masters inside {[1:16]};
    m_num_slaves  inside {[1:16]};
  }

  function new(string name = "dut_env_cfg");
    super.new(name);
  endfunction

  function void build();
    m_master_cfg_h = new[m_num_masters];
    foreach (m_master_cfg_h[i])
      m_master_cfg_h[i] = master_agent_cfg::type_id::create(
        $sformatf("m_master_cfg_h[%0d]", i));
    m_slave_cfg_h = new[m_num_slaves];
    foreach (m_slave_cfg_h[i])
      m_slave_cfg_h[i] = slave_agent_cfg::type_id::create(
        $sformatf("m_slave_cfg_h[%0d]", i));
  endfunction
endclass
```

---

## 5.8 Complete Environment Skeleton

```systemverilog
class dut_env extends uvm_env;
  `uvm_component_utils(dut_env)

  master_agent     m_master_agent_h[];
  slave_agent      m_slave_agent_h[];
  dut_scoreboard   m_scoreboard_h;
  dut_coverage     m_coverage_h;
  dut_env_cfg      m_cfg_h;

  function new(string name, uvm_component parent);
    super.new(name, parent);
  endfunction

  function void build_phase(uvm_phase phase);
    super.build_phase(phase);

    if (!uvm_config_db#(dut_env_cfg)::get(this, "", "m_cfg_h", m_cfg_h))
      `uvm_fatal(get_name(), "dut_env_cfg not found")

    m_master_agent_h = new[m_cfg_h.m_num_masters];
    foreach (m_master_agent_h[i]) begin
      uvm_config_db#(master_agent_cfg)::set(
        this, $sformatf("m_master_agent_h[%0d]*", i),
        "m_cfg_h", m_cfg_h.m_master_cfg_h[i]);
      m_master_agent_h[i] = master_agent::type_id::create(
        $sformatf("m_master_agent_h[%0d]", i), this);
    end

    if (m_cfg_h.m_has_scoreboard)
      m_scoreboard_h = dut_scoreboard::type_id::create("m_scoreboard_h", this);
    if (m_cfg_h.m_has_coverage)
      m_coverage_h   = dut_coverage::type_id::create("m_coverage_h", this);
  endfunction

  function void connect_phase(uvm_phase phase);
    foreach (m_master_agent_h[i]) begin
      if (m_cfg_h.m_has_scoreboard)
        m_master_agent_h[i].m_monitor_h.m_ap.connect(
          m_scoreboard_h.m_master_export);
      if (m_cfg_h.m_has_coverage)
        m_master_agent_h[i].m_monitor_h.m_ap.connect(
          m_coverage_h.m_analysis_export);
    end
  endfunction
endclass
```

---

## 5.9 UVM Coding Standards

| Standard | Rule |
|---|---|
| Member prefix | `m_` for all class members |
| Handle suffix | `_h` for all handles |
| Factory utils | Every class has `uvm_component_utils` or `uvm_object_utils` |
| Config db | All interfaces and configs via config_db — never direct |
| Rand fail | `uvm_fatal` on every failed `randomize()` call |
| Objections | Always raise before stimulus, always drop after drain |
| Fatal on null | Never use a null handle — check and fatal |
| No `$display` | Use `uvm_info/warning/error/fatal` only |
