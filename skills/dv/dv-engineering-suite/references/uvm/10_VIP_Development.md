# Module 10 — VIP Development
## Full VIP Architecture: Transaction/Protocol/Timing/Config/Coverage/Scoreboard

---

## 10.1 VIP Layer Architecture

```
┌─────────────────────────────────────────────┐
│               User Test/Sequence            │  API Layer
├─────────────────────────────────────────────┤
│          Protocol Sequence Library          │  Protocol Layer
│  (legal transactions, corner cases, reuse) │
├─────────────────────────────────────────────┤
│         Transaction (seq_item) Layer        │  Data Layer
│   (fields, constraints, convert2string)    │
├─────────────────────────────────────────────┤
│              Agent / Driver / Monitor       │  Verification Layer
├─────────────────────────────────────────────┤
│         Protocol Checker (SVA + bind)       │  Check Layer
├─────────────────────────────────────────────┤
│              Coverage Collector             │  Measure Layer
├─────────────────────────────────────────────┤
│              Scoreboard / Predictor         │  Compare Layer
├─────────────────────────────────────────────┤
│            Config Object + API              │  Config Layer
├─────────────────────────────────────────────┤
│              Physical Interface             │  Signal Layer
└─────────────────────────────────────────────┘
```

## 10.2 VIP Reuse Design Rules

| Rule | Rationale |
|---|---|
| Parameterize all widths | DATA_WIDTH, ADDR_WIDTH, ID_WIDTH |
| Config controls all behavior | No hardcoded modes |
| Protocol checker in bind block | Reusable without DUT modification |
| Coverage model in subscriber | Separable from agent |
| Scoreboard separate from agent | Can be reused across different TBs |
| All fields in seq_item | No hard-coded values in driver |
| Factory registration everywhere | Override without code change |
| Passive mode support | Monitor-only deployment at SoC level |

## 10.3 VIP Configuration Object Pattern

```systemverilog
class proto_vip_cfg extends uvm_object;
  `uvm_object_utils(proto_vip_cfg)

  // Interface
  virtual proto_if m_vif;

  // Active/passive
  uvm_active_passive_enum m_is_active = UVM_ACTIVE;

  // Protocol configuration
  int unsigned m_data_width = 64;
  int unsigned m_addr_width = 32;
  int unsigned m_id_width   = 8;
  int unsigned m_max_outstanding = 16;

  // Behavioral knobs
  bit m_enable_protocol_check = 1;
  bit m_enable_coverage       = 1;
  bit m_enable_scoreboard     = 1;
  int unsigned m_response_latency_min = 1;
  int unsigned m_response_latency_max = 64;

  // Randomization control
  bit m_enable_backpressure = 0;
  int unsigned m_backpressure_probability = 10; // percent
endclass
```

## 10.4 VIP Packaging Checklist

Before releasing VIP for reuse:
☐ README with API description, integration guide, example tests
☐ All widths parameterized
☐ Config object documented
☐ Factory registration on all classes
☐ Protocol checker in bind block with test vectors
☐ Coverage model with all cross bins
☐ Scoreboard with in-order AND OOO modes
☐ Negative test sequences included
☐ Performance measurement sequences included
☐ Regression suite: sanity + protocol compliance + stress
☐ Versioned release tag
