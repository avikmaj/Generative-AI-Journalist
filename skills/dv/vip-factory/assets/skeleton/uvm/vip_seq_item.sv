// =============================================================================
// AVIK VIP FACTORY — Reusable VIP Skeleton
// File: uvm/transaction/<vip>_seq_item.sv
// Item 11: Reusable VIP Skeleton — Transaction Layer
// USAGE: Search/replace <VIP> with your protocol name (e.g. AXI4, APB4)
//        Search/replace <vip> with lowercase (e.g. axi4, apb4)
// =============================================================================

class <vip>_seq_item extends uvm_sequence_item;
  `uvm_object_utils_begin(<vip>_seq_item)
    // Register all fields for copy/compare/print/record
    `uvm_field_int(m_addr,   UVM_ALL_ON)
    `uvm_field_int(m_data,   UVM_ALL_ON)
    `uvm_field_int(m_write,  UVM_ALL_ON)
    `uvm_field_int(m_delay,  UVM_ALL_ON)
    `uvm_field_enum(<vip>_txn_type_e, m_txn_type, UVM_ALL_ON)
  `uvm_object_utils_end

  // ── Transaction type ──────────────────────────────────────────────────────
  typedef enum {
    TXN_WRITE,
    TXN_READ,
    TXN_IDLE
  } <vip>_txn_type_e;

  // ── Randomizable fields ───────────────────────────────────────────────────
  rand <vip>_txn_type_e m_txn_type;
  rand logic [31:0]     m_addr;
  rand logic [31:0]     m_data;
  rand logic            m_write;
  rand int unsigned     m_delay;     // inter-transaction delay in cycles

  // ── Non-randomizable (response) fields ───────────────────────────────────
  logic [31:0]          m_rdata;     // read data from DUT
  logic [1:0]           m_resp;      // response code
  bit                   m_error;     // set by scoreboard on mismatch

  // ── Constraints ───────────────────────────────────────────────────────────
  constraint c_addr_valid {
    m_addr inside {[32'h0000_0000 : 32'hFFFF_FFFC]};
    m_addr[1:0] == 2'b00;            // word-aligned
  }

  constraint c_delay_dist {
    m_delay dist {0:=60, [1:4]:=30, [5:20]:=10};
  }

  constraint c_write_from_type {
    m_txn_type == TXN_WRITE -> m_write == 1;
    m_txn_type == TXN_READ  -> m_write == 0;
  }

  // ── Constructor ───────────────────────────────────────────────────────────
  function new(string name = "<vip>_seq_item");
    super.new(name);
  endfunction

  // ── Convert to string (for scoreboard messages) ───────────────────────────
  virtual function string convert2string();
    return $sformatf(
      "[%s] addr=0x%08h data=0x%08h write=%0b resp=%02b delay=%0d",
      m_txn_type.name(), m_addr, m_data, m_write, m_resp, m_delay);
  endfunction

  // ── do_compare override (used by scoreboard) ─────────────────────────────
  virtual function bit do_compare(uvm_object rhs, uvm_comparer comparer);
    <vip>_seq_item rhs_;
    if (!$cast(rhs_, rhs)) return 0;
    return (m_addr  == rhs_.m_addr  &&
            m_rdata == rhs_.m_rdata &&
            m_resp  == rhs_.m_resp);
  endfunction

endclass : <vip>_seq_item
