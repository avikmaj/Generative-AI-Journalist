// =============================================================================
// AVIK VIP FACTORY — Reusable VIP Skeleton
// File: uvm/pkg/<vip>_pkg.sv
// Item 11: Reusable VIP Skeleton — UVM Package
// =============================================================================

package <vip>_pkg;
  import uvm_pkg::*;
  `include "uvm_macros.svh"

  // Include all VIP classes in dependency order
  `include "<vip>_seq_item.sv"
  `include "<vip>_agent_cfg.sv"
  `include "<vip>_env_cfg.sv"
  `include "<vip>_sequencer.sv"
  `include "<vip>_driver.sv"
  `include "<vip>_monitor.sv"
  `include "<vip>_agent.sv"
  `include "<vip>_scoreboard.sv"
  `include "<vip>_coverage.sv"
  `include "<vip>_base_seq.sv"
  `include "<vip>_env.sv"
  `include "<vip>_base_test.sv"

endpackage : <vip>_pkg

// =============================================================================
// File: tb/<vip>_if.sv
// Item 11: Reusable VIP Skeleton — Virtual Interface
// =============================================================================

interface <vip>_if #(
  parameter DATA_WIDTH = 32,
  parameter ADDR_WIDTH = 32
)(
  input logic clk,
  input logic rst_n
);

  // ── Protocol signals — customize per VIP ──────────────────────────────────
  // TODO: replace with actual protocol signals

  logic                    valid;
  logic                    ready;
  logic [ADDR_WIDTH-1:0]   addr;
  logic [DATA_WIDTH-1:0]   wdata;
  logic [DATA_WIDTH-1:0]   rdata;
  logic                    write;
  logic [1:0]              resp;

  // ── Modports ──────────────────────────────────────────────────────────────

  modport master_mp (
    output valid, addr, wdata, write,
    input  ready, rdata, resp,
    input  clk, rst_n
  );

  modport slave_mp (
    input  valid, addr, wdata, write,
    output ready, rdata, resp,
    input  clk, rst_n
  );

  modport monitor_mp (
    input valid, ready, addr, wdata, rdata, write, resp,
    input clk, rst_n
  );

  // ── Clocking blocks (avoids TB races) ─────────────────────────────────────

  clocking master_cb @(posedge clk);
    default input  #1step;
    default output #1;
    input  ready, rdata, resp;
    output valid, addr, wdata, write;
  endclocking

  clocking monitor_cb @(posedge clk);
    default input #1step;
    input valid, ready, addr, wdata, rdata, write, resp;
  endclocking

endinterface : <vip>_if

// =============================================================================
// File: tb/tb_top.sv
// Item 11: Reusable VIP Skeleton — Testbench Top
// =============================================================================

`timescale 1ns/1ps

module tb_top;
  import uvm_pkg::*;
  `include "uvm_macros.svh"
  import <vip>_pkg::*;

  // ── Clock and reset ───────────────────────────────────────────────────────
  logic clk;
  logic rst_n;

  initial clk = 0;
  always #5 clk = ~clk;   // 100MHz

  initial begin
    rst_n = 0;
    repeat(10) @(posedge clk);
    rst_n = 1;
    `uvm_info("TB_TOP", "Reset released", UVM_NONE)
  end

  // ── Interface instantiation ───────────────────────────────────────────────
  <vip>_if #(
    .DATA_WIDTH(32),
    .ADDR_WIDTH(32)
  ) u_<vip>_if (.clk(clk), .rst_n(rst_n));

  // ── DUT instantiation ─────────────────────────────────────────────────────
  // TODO: replace with actual DUT
  // <dut_module> u_dut (
  //   .clk    (u_<vip>_if.clk),
  //   .rst_n  (u_<vip>_if.rst_n),
  //   .valid  (u_<vip>_if.valid),
  //   .ready  (u_<vip>_if.ready),
  //   ...
  // );

  // ── Bind protocol checker ─────────────────────────────────────────────────
  // bind <dut_module> <vip>_protocol_checker u_checker (
  //   .clk   (clk),
  //   .rst_n (rst_n)
  // );

  // ── UVM configuration and start ──────────────────────────────────────────
  initial begin
    // Pass virtual interface to UVM config_db
    uvm_config_db#(virtual <vip>_if)::set(
      null, "uvm_test_top.*", "m_vif", u_<vip>_if);

    // Start UVM test
    run_test();
  end

  // ── Timeout watchdog ─────────────────────────────────────────────────────
  initial begin
    #10_000_000ns;   // 10ms timeout
    `uvm_fatal("TIMEOUT", "Simulation exceeded 10ms — possible deadlock")
  end

endmodule : tb_top

// =============================================================================
// File: tb/filelist.f
// Item 11: Reusable VIP Skeleton — Filelist
// =============================================================================
// Usage: verilator --sv -f tb/filelist.f
//
// +incdir+$UVM_HOME/src
// $UVM_HOME/src/uvm_pkg.sv
//
// // Interface
// tb/<vip>_if.sv
//
// // DUT (under test)
// rtl/<dut>.sv
//
// // VIP package (includes all UVM classes)
// uvm/pkg/<vip>_pkg.sv
//
// // Testbench top
// tb/tb_top.sv
//
// // Tests (specify active test via +UVM_TESTNAME)
// tests/<vip>_base_test.sv
// tests/<vip>_smoke_test.sv
// tests/<vip>_write_test.sv
// tests/<vip>_read_test.sv
// tests/<vip>_random_test.sv
// tests/<vip>_error_test.sv
// tests/<vip>_stress_test.sv
