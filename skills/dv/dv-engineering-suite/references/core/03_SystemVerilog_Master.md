# Module 03 — SystemVerilog Master
## Interfaces · Clocking Blocks · Data Types · OOP · Concurrency

---

## 3.1 Interfaces

```systemverilog
interface axi4_if #(parameter DATA_WIDTH=64, ADDR_WIDTH=32, ID_WIDTH=8) (input logic clk, rst_n);
  // Write address channel
  logic [ID_WIDTH-1:0]   awid;
  logic [ADDR_WIDTH-1:0] awaddr;
  logic [7:0]            awlen;
  logic [2:0]            awsize;
  logic [1:0]            awburst;
  logic                  awvalid, awready;
  // Write data channel
  logic [DATA_WIDTH-1:0]   wdata;
  logic [DATA_WIDTH/8-1:0] wstrb;
  logic                    wlast, wvalid, wready;
  // Write response channel
  logic [ID_WIDTH-1:0] bid;
  logic [1:0]          bresp;
  logic                bvalid, bready;

  // Master modport — drives AW/W, receives B
  modport master (
    output awid, awaddr, awlen, awsize, awburst, awvalid,
    input  awready,
    output wdata, wstrb, wlast, wvalid,
    input  wready,
    input  bid, bresp, bvalid,
    output bready,
    input  clk, rst_n
  );

  // Slave modport — receives AW/W, drives B
  modport slave (
    input  awid, awaddr, awlen, awsize, awburst, awvalid,
    output awready,
    input  wdata, wstrb, wlast, wvalid,
    output wready,
    output bid, bresp, bvalid,
    input  bready,
    input  clk, rst_n
  );

  // Clocking block for TB sampling (avoids races)
  clocking master_cb @(posedge clk);
    default input  #1step;
    default output #1;
    input  awready, wready, bvalid, bid, bresp;
    output awid, awaddr, awlen, awsize, awburst, awvalid;
    output wdata, wstrb, wlast, wvalid;
    output bready;
  endclocking
endinterface
```

## 3.2 Key Data Types

| Type | Use | Notes |
|---|---|---|
| `logic` | Any net/variable | Replaces `wire` and `reg` |
| `bit` | 2-state | Faster simulation, no X/Z |
| `byte` | 8-bit 2-state signed | |
| `int` | 32-bit 2-state signed | |
| `longint` | 64-bit 2-state signed | |
| `string` | Dynamic string | UVM messages |
| `typedef enum` | Named states | FSM encoding |
| `struct packed` | Bit-packed struct | Register fields |
| `union packed` | Overlapping fields | Register access |
| `queue[$]` | Dynamic FIFO | Scoreboard |
| `assoc array[key]` | Hash map | OOO scoreboard |
| `dynamic array[]` | Resizable array | Parameterized |

## 3.3 Randomization

```systemverilog
class axi_seq_item extends uvm_sequence_item;
  `uvm_object_utils(axi_seq_item)

  rand logic [7:0]  awlen;
  rand logic [1:0]  awburst;
  rand logic [2:0]  awsize;
  rand logic [31:0] awaddr;
  rand int unsigned m_delay;

  // Distribution constraint
  constraint c_burst_dist {
    awburst dist {2'b00:=10, 2'b01:=70, 2'b10:=20};
  }

  // Conditional constraint
  constraint c_wrap_len {
    awburst == 2'b10 -> awlen inside {8'h01, 8'h03, 8'h07, 8'h0F};
  }

  // Solve ordering
  constraint c_size_addr {
    solve awsize before awaddr;
    awaddr[awsize-1:0] == 0; // aligned
  }
endclass

// Usage
if (!req.randomize() with { awburst == 2'b10; awlen == 8'hFF; })
  `uvm_fatal(get_name(), "Randomization failed")
```

## 3.4 OOP Patterns

```systemverilog
// Inheritance
class axi_write_seq extends axi_base_seq;
  `uvm_object_utils(axi_write_seq)
  // Override parent body()
  task body();
    super.body(); // call parent if needed
    // extended behavior
  endtask
endclass

// Polymorphism
class base_checker extends uvm_component;
  virtual function void check_response(my_item t);
    // base implementation
  endfunction
endclass

class extended_checker extends base_checker;
  virtual function void check_response(my_item t);
    super.check_response(t);
    // additional checks
  endfunction
endclass
```
