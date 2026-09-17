# Module 09 — RAL Register Model
## uvm_reg · Frontdoor/Backdoor · Adapter · Predictor · Sequences

---

## 9.1 Register Model

```systemverilog
class dut_ctrl_reg extends uvm_reg;
  `uvm_object_utils(dut_ctrl_reg)

  rand uvm_reg_field m_enable;
  rand uvm_reg_field m_mode;
  rand uvm_reg_field m_reserved;

  function new(string name = "dut_ctrl_reg");
    super.new(name, 32, UVM_NO_COVERAGE);
  endfunction

  virtual function void build();
    m_enable   = uvm_reg_field::type_id::create("m_enable");
    m_mode     = uvm_reg_field::type_id::create("m_mode");
    m_reserved = uvm_reg_field::type_id::create("m_reserved");

    m_enable.configure(this, 1, 0, "RW", 0, 1'b0, 1, 1, 0);
    m_mode.configure(  this, 3, 1, "RW", 0, 3'b000, 1, 1, 0);
    m_reserved.configure(this, 28, 4, "RO", 0, 28'h0, 1, 0, 0);
  endfunction
endclass

class dut_reg_block extends uvm_reg_block;
  `uvm_object_utils(dut_reg_block)
  rand dut_ctrl_reg m_ctrl_reg;

  function new(string name = "dut_reg_block");
    super.new(name, UVM_NO_COVERAGE);
  endfunction

  virtual function void build();
    m_ctrl_reg = dut_ctrl_reg::type_id::create("m_ctrl_reg");
    m_ctrl_reg.build();
    m_ctrl_reg.configure(this, null, "");
    default_map = create_map("default_map", 0, 4, UVM_LITTLE_ENDIAN);
    default_map.add_reg(m_ctrl_reg, 32'h0000, "RW");
    lock_model();
  endfunction
endclass
```

## 9.2 Register Sequences

```systemverilog
// Write and read back
task test_reg_write_read(dut_reg_block ral, uvm_status_e status);
  uvm_reg_data_t wdata, rdata;
  wdata = 32'hDEAD_BEEF;
  ral.m_ctrl_reg.write(status, wdata);
  if (status != UVM_IS_OK) `uvm_error("RAL", "Write failed")
  ral.m_ctrl_reg.read(status, rdata);
  if (rdata !== wdata) `uvm_error("RAL", $sformatf("Mismatch: exp=%0h got=%0h", wdata, rdata))
endtask

// Built-in register tests
// uvm_reg_hw_reset_seq  — check reset values
// uvm_reg_bit_bash_seq  — walk-ones through each field
// uvm_reg_access_seq    — write/readback all registers
```
