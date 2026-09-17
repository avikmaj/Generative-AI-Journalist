# Module 07 — UVM Sequences
## sequence_item · Layered · Virtual · p_sequencer · Libraries

---

## 7.1 Sequence Item

```systemverilog
class axi_seq_item extends uvm_sequence_item;
  `uvm_object_utils_begin(axi_seq_item)
    `uvm_field_int(awaddr,  UVM_ALL_ON)
    `uvm_field_int(awlen,   UVM_ALL_ON)
    `uvm_field_int(awburst, UVM_ALL_ON)
  `uvm_object_utils_end

  rand logic [31:0] awaddr;
  rand logic [7:0]  awlen;
  rand logic [1:0]  awburst;
  rand logic [2:0]  awsize;

  constraint c_burst_valid { awburst != 2'b11; }

  function string convert2string();
    return $sformatf("addr=0x%08h len=%0d burst=%0b size=%0d",
                     awaddr, awlen, awburst, awsize);
  endfunction
endclass
```

## 7.2 Base Sequence Pattern

```systemverilog
class axi_base_seq extends uvm_sequence#(axi_seq_item);
  `uvm_object_utils(axi_base_seq)
  `uvm_declare_p_sequencer(axi_sequencer)

  int unsigned m_num_txn = 10;

  task body();
    axi_seq_item req;
    if (starting_phase != null) starting_phase.raise_objection(this);
    repeat(m_num_txn) begin
      req = axi_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize()) `uvm_fatal(get_name(), "Randomization failed")
      finish_item(req);
    end
    if (starting_phase != null) starting_phase.drop_objection(this);
  endtask
endclass
```

## 7.3 Virtual Sequence

```systemverilog
class tb_virtual_sequencer extends uvm_sequencer;
  `uvm_component_utils(tb_virtual_sequencer)
  master_sequencer m_master_seqr_h[];
  slave_sequencer  m_slave_seqr_h[];
endclass

class tb_virtual_seq extends uvm_sequence;
  `uvm_object_utils(tb_virtual_seq)
  `uvm_declare_p_sequencer(tb_virtual_sequencer)

  task body();
    master_seq m_seq[];
    slave_rsp_seq s_seq;
    m_seq = new[p_sequencer.m_master_seqr_h.size()];
    s_seq = slave_rsp_seq::type_id::create("s_seq");

    fork
      foreach(m_seq[i]) begin
        automatic int j = i;
        m_seq[j] = master_seq::type_id::create($sformatf("m_seq[%0d]",j));
        m_seq[j].start(p_sequencer.m_master_seqr_h[j]);
      end
      s_seq.start(p_sequencer.m_slave_seqr_h[0]);
    join
  endtask
endclass
```
