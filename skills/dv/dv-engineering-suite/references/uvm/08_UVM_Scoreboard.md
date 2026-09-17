# Module 08 — UVM Scoreboard Architecture
## In-Order · Out-of-Order · Reference Model · Predictors

---

## 8.1 In-Order Scoreboard

```systemverilog
`uvm_analysis_imp_decl(_stim)
`uvm_analysis_imp_decl(_resp)

class dut_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(dut_scoreboard)

  uvm_analysis_imp_stim#(my_item, dut_scoreboard) m_stim_export;
  uvm_analysis_imp_resp#(my_item, dut_scoreboard) m_resp_export;

  my_item m_expected_q[$];
  int m_match=0, m_error=0;

  function void write_stim(my_item t);
    my_item exp = my_item::type_id::create("exp");
    predict(t, exp);           // compute expected output
    m_expected_q.push_back(exp);
  endfunction

  function void write_resp(my_item t);
    if (m_expected_q.size()==0) begin
      `uvm_error(get_name(), "Unexpected response"); m_error++; return;
    end
    my_item exp = m_expected_q.pop_front();
    if (!t.compare(exp)) begin
      `uvm_error(get_name(), $sformatf("MISMATCH:\nExp: %s\nAct: %s",
        exp.convert2string(), t.convert2string()));
      m_error++;
    end else m_match++;
  endfunction

  virtual function void predict(my_item stim, ref my_item exp);
    // Implement DUT functional model here
    exp.data = stim.data; // placeholder
  endfunction
endclass
```

## 8.2 Out-of-Order Scoreboard (ID-based)

```systemverilog
class ooo_scoreboard extends uvm_scoreboard;
  `uvm_component_utils(ooo_scoreboard)
  // Key = transaction ID, value = expected response
  my_item m_expected_aa[int];

  function void write_stim(my_item t);
    my_item exp = my_item::type_id::create("exp");
    predict(t, exp);
    if (m_expected_aa.exists(t.id))
      `uvm_error(get_name(), $sformatf("ID collision: id=%0h", t.id))
    m_expected_aa[t.id] = exp;
  endfunction

  function void write_resp(my_item t);
    if (!m_expected_aa.exists(t.id)) begin
      `uvm_error(get_name(), $sformatf("Response with no prediction: id=%0h", t.id))
      return;
    end
    my_item exp = m_expected_aa[t.id];
    m_expected_aa.delete(t.id);
    if (!t.compare(exp))
      `uvm_error(get_name(), $sformatf("OOO MISMATCH id=%0h", t.id));
  endfunction
endclass
```
