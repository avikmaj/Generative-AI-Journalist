# Module 11 — AMBA Protocols
## AXI3/4/5 · ACE · CHI · AHB · APB · AXI-Stream · Complete DV Reference

---

## 11.1 AMBA Protocol Family Overview

```
AMBA Protocol Hierarchy
├── AXI (Advanced eXtensible Interface)
│   ├── AXI3          — 2003, IDs, bursts, 4KB limit
│   ├── AXI4          — 2010, 256-beat max, no write interleave
│   ├── AXI4-Lite     — 2010, single beat, no burst, no IDs
│   ├── AXI5          — 2017, atomics, poison, trace
│   └── AXI-Stream    — unidirectional data streaming
├── ACE (AXI Coherency Extensions)
│   ├── ACE           — full cache coherency
│   └── ACE-Lite      — I/O coherency (no snoop)
├── CHI (Coherent Hub Interface)
│   ├── CHI-A/B       — AMBA 5, ring/mesh NoC
│   └── CHI-E         — 2022, enhanced features
├── AHB (Advanced High-performance Bus)
│   ├── AHB           — legacy, shared bus
│   └── AHB5          — 2015, exclusives, memory attributes
└── APB (Advanced Peripheral Bus)
    ├── APB3          — wait states, error response
    └── APB4          — protection, strobe
```

---

## 11.2 AXI4 — Complete DV Reference

### Channel Architecture
```
Write Address Channel (AW): AWID, AWADDR, AWLEN, AWSIZE, AWBURST,
                             AWLOCK, AWCACHE, AWPROT, AWQOS, AWREGION, AWUSER
                             AWVALID, AWREADY

Write Data Channel (W):     WDATA, WSTRB, WLAST, WUSER, WVALID, WREADY

Write Response Channel (B): BID, BRESP, BUSER, BVALID, BREADY

Read Address Channel (AR):  ARID, ARADDR, ARLEN, ARSIZE, ARBURST,
                             ARLOCK, ARCACHE, ARPROT, ARQOS, ARREGION, ARUSER
                             ARVALID, ARREADY

Read Data Channel (R):      RID, RDATA, RRESP, RLAST, RUSER, RVALID, RREADY
```

### Key Parameters
| Parameter | AXI3 | AXI4 |
|---|---|---|
| Max burst length | 16 | 256 |
| Write interleaving | Supported | REMOVED |
| ID width | Flexible | Flexible |
| Atomic operations | No | No (AXI5) |
| QoS | No | Yes |

### AXI4 Handshake Protocol
```
VALID/READY handshake rules (CRITICAL — SVA must check all):

1. Master asserts VALID when data/addr available
2. Slave asserts READY when ready to accept
3. Transfer occurs on cycle where VALID AND READY both HIGH
4. VALID must NOT be deasserted without transfer (protocol violation)
5. READY can be deasserted at any time
6. Neither side shall wait for other to assert first (deadlock hazard)
```

### Burst Types
| AWBURST | Type | Address calculation |
|---|---|---|
| 2'b00 | FIXED | Same address every beat |
| 2'b01 | INCR | Increment by beat size |
| 2'b10 | WRAP | Wraps at boundary |
| 2'b11 | Reserved | Protocol violation |

### AWSIZE Encoding
| AWSIZE | Beat width |
|---|---|
| 3'h0 | 1 byte |
| 3'h1 | 2 bytes |
| 3'h2 | 4 bytes |
| 3'h3 | 8 bytes |
| 3'h4 | 16 bytes |
| 3'h5 | 32 bytes |
| 3'h6 | 64 bytes |
| 3'h7 | 128 bytes |

### BRESP / RRESP Encoding
| Code | Response | Meaning |
|---|---|---|
| 2'b00 | OKAY | Normal successful completion |
| 2'b01 | EXOKAY | Exclusive access successful |
| 2'b10 | SLVERR | Slave error |
| 2'b11 | DECERR | Decode error — no slave at address |

---

## 11.3 AXI4 Coverage Model

```systemverilog
covergroup axi4_write_cg @(posedge clk iff (awvalid && awready));
  option.per_instance = 1;

  // Burst length coverage
  cp_awlen: coverpoint awlen {
    bins len_1    = {8'h00};
    bins len_2_4  = {[8'h01:8'h03]};
    bins len_16   = {8'h0F};
    bins len_256  = {8'hFF};
    bins len_other = default;
  }

  // Burst type coverage
  cp_awburst: coverpoint awburst {
    bins FIXED = {2'b00};
    bins INCR  = {2'b01};
    bins WRAP  = {2'b10};
  }

  // Transfer size
  cp_awsize: coverpoint awsize {
    bins byte_1   = {3'h0};
    bins byte_4   = {3'h2};
    bins byte_64  = {3'h6};
    bins byte_128 = {3'h7};
  }

  // Cross: burst type × length
  cx_burst_len: cross cp_awlen, cp_awburst {
    // WRAP: only power-of-2 lengths valid
    illegal_bins wrap_invalid_len =
      binsof(cp_awburst.WRAP) && !binsof(cp_awlen.len_1)
      && !binsof(cp_awlen.len_16);
  }

  // Outstanding IDs
  cp_awid: coverpoint awid[3:0] {
    bins id[] = {[0:15]};
  }
endgroup

// Backpressure coverage
covergroup axi4_backpressure_cg @(posedge clk);
  option.per_instance = 1;

  cp_awready_deassert: coverpoint awready {
    bins deassert = (1 => 0);
    bins reassert = (0 => 1);
  }

  cp_wready_deassert: coverpoint wready {
    bins deassert = (1 => 0);
    bins reassert = (0 => 1);
  }

  cp_bready_deassert: coverpoint bready {
    bins deassert = (1 => 0);
  }
endgroup
```

---

## 11.4 AXI4 SVA Properties

```systemverilog
// Default clocking block
default clocking axi_clk @(posedge clk); endclocking
default disable iff (!rst_n);

// AWVALID must not deassert without handshake
property p_awvalid_stable;
  awvalid && !awready |=> awvalid;
endproperty
AWVALID_STABLE: assert property(p_awvalid_stable)
  else `uvm_error("SVA", "AWVALID deasserted without AWREADY");

// WLAST must assert on last beat
property p_wlast_on_last_beat;
  logic [7:0] len;
  (awvalid && awready, len = awlen) |->
  ##[1:$] (wvalid && wready && wlast, $past(wlast,0));
endproperty

// No BVALID without completed write
property p_bvalid_after_write;
  bvalid |-> $past(wlast && wvalid && wready, 1, 0, clk);
endproperty

// BRESP must be OKAY or SLVERR (not reserved)
property p_bresp_valid;
  bvalid |-> bresp inside {2'b00, 2'b01, 2'b10, 2'b11};
endproperty
```

---

## 11.5 AXI4 Corner Cases

**Must be in every AXI4 vplan:**

| Corner Case | Risk | Test Type |
|---|---|---|
| AWLEN=255 + WRAP burst | HIGH | Directed |
| Narrow burst (AWSIZE < data width) | HIGH | Directed + CRV |
| Unaligned address | HIGH | CRV |
| AWVALID/WVALID simultaneous deassert | HIGH | Directed |
| Outstanding transactions = max ID width | HIGH | CRV |
| BREADY deassert = 1000 cycles | MEDIUM | Directed |
| Write data before write address | MEDIUM | Directed |
| Back-to-back WRAP bursts | HIGH | CRV |
| SLVERR during burst (not last beat) | HIGH | Directed |
| Same ID, multiple outstanding | HIGH | CRV |
| Exclusive access sequences | MEDIUM | Directed |
| QoS = 0xF + QoS = 0x0 simultaneous | LOW | CRV |

---

## 11.6 CHI — Coherent Hub Interface

### Network Architecture
```
Request Node (RN) ─── CHI ───┐
                              │
Fully Coherent (RN-F) ──────┤
IO Coherent   (RN-I) ───────┤  Network-on-Chip
                              │  (interconnect)
Home Node (HN-F/HN-I) ──────┤
                              │
Slave Node (SN-F) ──────────┘
```

### CHI Channels
| Channel | Direction | Abbreviation | Purpose |
|---|---|---|---|
| REQ | RN → HN | TXREQ | Request (read, write, snoop response) |
| DAT | Bidirectional | TXDAT/RXDAT | Data |
| RSP | Bidirectional | TXRSP/RXRSP | Response, completion, acknowledge |
| SNP | HN → RN | RXSNP | Snoop request |

### CHI Transaction Types
| Type | Opcode | Description |
|---|---|---|
| ReadNoSnp | 0x0 | Non-coherent read |
| ReadOnce | 0x1 | Coherent read, not cached |
| ReadClean | 0x2 | Read, receive clean copy |
| ReadNotSharedDirty | 0x3 | Read, cannot be dirty |
| ReadShared | 0x4 | Shared read |
| ReadUnique | 0x5 | Exclusive read |
| WriteNoSnpFull | 0x10 | Non-coherent full cacheline write |
| WriteUniqueFull | 0x15 | Unique write, full cacheline |
| WriteBackFull | 0x12 | Writeback full cacheline |
| Evict | 0x16 | Evict clean cacheline |

### CHI Debug Anchors
```
TXREQ flit not ACKed    → Check credit return from HN
DAT flit arrives OOO    → Check TxnID ordering at HN
RetryAck received       → Check PCrdGrant before retry
Snoop not responded     → Check RN-F snoop machine
DBID not returned       → HN cannot accept new write
```

---

## 11.7 AHB5

### Signal Set
```
HCLK, HRESETn
HSEL, HADDR[31:0], HTRANS[1:0], HWRITE, HSIZE[2:0], HBURST[2:0]
HWDATA, HRDATA, HREADYOUT, HRESP, HMASTLOCK, HPROT[6:0]
HMASTER[3:0] (multi-master), HEXCL (exclusive)
```

### HTRANS Encoding
| HTRANS | Type | Description |
|---|---|---|
| 2'b00 | IDLE | No transfer |
| 2'b01 | BUSY | Master not ready (burst continuation) |
| 2'b10 | NONSEQ | First beat of burst or single |
| 2'b11 | SEQ | Subsequent burst beats |

### AHB Error Response (Two-Cycle)
```
Cycle 1: HRESP = ERROR, HREADYOUT = 0  (must hold)
Cycle 2: HRESP = ERROR, HREADYOUT = 1  (transfer complete)
```

**Single-cycle ERROR is a protocol violation — SVA must catch.**

---

## 11.8 APB4

### Signal Set
```
PCLK, PRESETn
PSEL, PENABLE, PWRITE, PADDR[31:0], PWDATA[31:0]
PRDATA[31:0], PREADY, PSLVERR
PPROT[2:0], PSTRB[3:0]  (APB4 additions)
```

### APB Transfer Phases
```
SETUP Phase:    PSEL=1, PENABLE=0 — one clock cycle always
ACCESS Phase:   PSEL=1, PENABLE=1 — extended by PREADY=0
IDLE:           PSEL=0, PENABLE=0
```

### APB Coverage Model
```systemverilog
covergroup apb_cg @(posedge PCLK iff (PSEL && PENABLE && PREADY));
  cp_rw:     coverpoint PWRITE { bins read=0; bins write=1; }
  cp_strobe: coverpoint PSTRB {
    bins all_bytes = {4'hF};
    bins single[]  = {4'h1, 4'h2, 4'h4, 4'h8};
    bins partial   = default;
  }
  cp_error:  coverpoint PSLVERR { bins ok=0; bins err=1; }
  cp_wait:   coverpoint $countones(PREADY==0) {
    bins no_wait    = {0};
    bins short_wait = {[1:4]};
    bins long_wait  = {[5:$]};
  }
  cx_rw_err: cross cp_rw, cp_error;
endgroup
```

---

## 11.9 AXI-Stream

### Signal Set
```
ACLK, ARESETn
TVALID, TREADY, TDATA[N-1:0], TSTRB[(N/8)-1:0]
TKEEP[(N/8)-1:0], TLAST, TID[7:0], TDEST[7:0], TUSER
```

### Key Rules
- TLAST marks end of packet (frame/burst)
- TSTRB: byte position contains data, not padding
- TKEEP: byte position is part of the packet
- TDEST: routing — crossbar destination
- No address channel — purely streaming

### AXI-Stream Corner Cases
| Case | Risk |
|---|---|
| TLAST deassert in middle of packet | HIGH |
| TKEEP all zeros without TLAST | MEDIUM |
| TDEST changes within packet | HIGH |
| Backpressure (TREADY=0) for 1000 cycles | MEDIUM |
| Zero-byte packet (TVALID without data) | LOW |
