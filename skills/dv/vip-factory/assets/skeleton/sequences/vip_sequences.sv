// =============================================================================
// AVIK VIP FACTORY — Reusable Sequence Templates
// Item 12: Reusable test/sequence templates
// =============================================================================

// =============================================================================
// BASE SEQUENCE — parent for all VIP sequences
// =============================================================================

class <vip>_base_seq extends uvm_sequence#(<vip>_seq_item);
  `uvm_object_utils(<vip>_base_seq)
  `uvm_declare_p_sequencer(<vip>_sequencer)

  int unsigned m_num_transactions = 10;

  function new(string name = "<vip>_base_seq");
    super.new(name);
  endfunction

  task body();
    if (starting_phase != null)
      starting_phase.raise_objection(this, "base_seq running");
    run_sequence();
    if (starting_phase != null)
      starting_phase.drop_objection(this, "base_seq done");
  endtask

  virtual task run_sequence();
    // Override in derived sequences
  endtask

  // Utility: create, randomize, and send one item with constraints
  task send_item(ref <vip>_seq_item req);
    start_item(req);
    if (!req.randomize())
      `uvm_fatal(get_name(), "Randomization failed — check constraints")
    finish_item(req);
  endtask

  // Utility: send item with inline constraints
  task send_constrained(ref <vip>_seq_item req, input string constraint_str = "");
    start_item(req);
    if (!req.randomize())
      `uvm_fatal(get_name(), $sformatf("Randomization failed [%s]", constraint_str))
    finish_item(req);
  endtask

endclass : <vip>_base_seq

// =============================================================================
// WRITE SEQUENCE — directed write transactions
// =============================================================================

class <vip>_write_seq extends <vip>_base_seq;
  `uvm_object_utils(<vip>_write_seq)

  rand logic [31:0] m_start_addr = 32'h0000_0000;
  rand logic [31:0] m_data_seed  = 32'hDEAD_BEEF;

  function new(string name = "<vip>_write_seq");
    super.new(name);
  endfunction

  virtual task run_sequence();
    <vip>_seq_item req;
    repeat(m_num_transactions) begin
      req = <vip>_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize() with {
        m_txn_type == <vip>_seq_item::TXN_WRITE;
        m_write    == 1;
        m_addr     inside {[m_start_addr : m_start_addr + 32'hFF]};
      }) `uvm_fatal(get_name(), "Write seq randomization failed")
      finish_item(req);
    end
  endtask

endclass : <vip>_write_seq

// =============================================================================
// READ SEQUENCE — directed read transactions
// =============================================================================

class <vip>_read_seq extends <vip>_base_seq;
  `uvm_object_utils(<vip>_read_seq)

  rand logic [31:0] m_start_addr = 32'h0000_0000;

  function new(string name = "<vip>_read_seq");
    super.new(name);
  endfunction

  virtual task run_sequence();
    <vip>_seq_item req;
    repeat(m_num_transactions) begin
      req = <vip>_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize() with {
        m_txn_type == <vip>_seq_item::TXN_READ;
        m_write    == 0;
        m_addr     inside {[m_start_addr : m_start_addr + 32'hFF]};
      }) `uvm_fatal(get_name(), "Read seq randomization failed")
      finish_item(req);
    end
  endtask

endclass : <vip>_read_seq

// =============================================================================
// RANDOM SEQUENCE — constrained-random, coverage-driven
// =============================================================================

class <vip>_random_seq extends <vip>_base_seq;
  `uvm_object_utils(<vip>_random_seq)

  // Knobs — configurable per test
  int unsigned m_max_outstanding  = 1;
  bit          m_enable_backpressure = 0;

  // Distribution weights — tune for coverage closure
  int unsigned m_write_weight = 50;
  int unsigned m_read_weight  = 50;

  function new(string name = "<vip>_random_seq");
    super.new(name);
  endfunction

  virtual task run_sequence();
    <vip>_seq_item req;
    repeat(m_num_transactions) begin
      req = <vip>_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize() with {
        m_txn_type dist {
          <vip>_seq_item::TXN_WRITE :/ m_write_weight,
          <vip>_seq_item::TXN_READ  :/ m_read_weight
        };
      }) `uvm_fatal(get_name(), "Random seq randomization failed")
      finish_item(req);
    end
  endtask

endclass : <vip>_random_seq

// =============================================================================
// ERROR SEQUENCE — protocol violation injection (negative tests)
// Expected result: protocol checker fires = EXPECTED_FAILURE_DETECTED
// =============================================================================

class <vip>_error_seq extends <vip>_base_seq;
  `uvm_object_utils(<vip>_error_seq)

  typedef enum {
    ERR_ILLEGAL_ADDR,
    ERR_ILLEGAL_CMD,
    ERR_PROTOCOL_VIOLATION
  } <vip>_error_type_e;

  rand <vip>_error_type_e m_error_type;

  function new(string name = "<vip>_error_seq");
    super.new(name);
  endfunction

  virtual task run_sequence();
    <vip>_seq_item req;
    `uvm_info(get_name(),
      $sformatf("NEGATIVE SEQ: injecting error type %s", m_error_type.name()),
      UVM_NONE)

    req = <vip>_seq_item::type_id::create("req");
    start_item(req);

    case (m_error_type)
      ERR_ILLEGAL_ADDR: begin
        if (!req.randomize() with {
          // TODO: inject protocol-specific illegal address
          // e.g. m_addr[1:0] != 2'b00;  // unaligned
        }) `uvm_fatal(get_name(), "Error seq randomization failed")
      end
      ERR_ILLEGAL_CMD: begin
        if (!req.randomize() with {
          // TODO: inject illegal command encoding
        }) `uvm_fatal(get_name(), "Error seq randomization failed")
      end
      default: begin
        if (!req.randomize())
          `uvm_fatal(get_name(), "Error seq randomization failed")
      end
    endcase

    finish_item(req);
    // Expected: assertion fires, scoreboard sees PROTOCOL_VIOLATION
    // Status in result.json: EXPECTED_FAILURE_DETECTED = PASS
  endtask

endclass : <vip>_error_seq

// =============================================================================
// BACKPRESSURE SEQUENCE — READY deassert scenarios
// =============================================================================

class <vip>_backpressure_seq extends <vip>_base_seq;
  `uvm_object_utils(<vip>_backpressure_seq)

  // Backpressure duration range
  rand int unsigned m_bp_min_cycles = 1;
  rand int unsigned m_bp_max_cycles = 20;

  constraint c_bp_valid {
    m_bp_min_cycles <= m_bp_max_cycles;
    m_bp_max_cycles <= 100;
  }

  function new(string name = "<vip>_backpressure_seq");
    super.new(name);
  endfunction

  virtual task run_sequence();
    <vip>_seq_item req;
    int unsigned bp_cycles;
    repeat(m_num_transactions) begin
      req = <vip>_seq_item::type_id::create("req");
      start_item(req);
      if (!req.randomize())
        `uvm_fatal(get_name(), "Backpressure seq randomization failed")
      // Inject backpressure via delay field
      req.m_delay = $urandom_range(m_bp_min_cycles, m_bp_max_cycles);
      finish_item(req);
    end
  endtask

endclass : <vip>_backpressure_seq
