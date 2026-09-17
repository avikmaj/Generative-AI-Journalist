# VIP DEVELOPMENT PLAN
## AVIK VIP Factory · Factory Structure · Roadmap · Per-VIP Lifecycle

---

## Factory Directory Structure

```
AVIK_VIP_FACTORY/
│
├── CLAUDE.md                    ← master team rules (this project)
├── VIP_DEVELOPMENT_PLAN.md      ← this file
├── policy/
│   ├── PASS_FAIL_POLICY.md
│   ├── REGRESSION_POLICY.md
│   └── SIMULATOR_POLICY.md
│
├── templates/
│   ├── VIP_TESTPLAN_TEMPLATE.md
│   ├── VIP_SIGNOFF_TEMPLATE.md
│   ├── vip_skeleton/            ← copy for each new VIP
│   └── test_skeleton/
│
├── common/                      ← shared across all VIPs
│   ├── uvm_pkg/
│   │   ├── common_seq_item.sv
│   │   ├── common_reporter.sv
│   │   └── common_pkg.sv
│   ├── utils/
│   │   ├── result_parser.py
│   │   └── coverage_utils.py
│   └── macros/
│       └── dv_macros.svh
│
├── vip/                         ← one directory per VIP
│   ├── axi4/
│   ├── axi4lite/
│   ├── axi3/
│   ├── axi_stream/
│   ├── ahb5/
│   ├── apb4/
│   ├── ace/
│   ├── chi/
│   └── <future>/
│
├── dv_runner/                   ← unified execution interface
│   ├── dv_runner.py
│   ├── compile.py
│   ├── simulate.py
│   ├── regression.py
│   ├── result_parser.py
│   ├── coverage.py
│   └── waveform.py
│
├── regression_db/               ← all historical results
├── results/                     ← current run results
├── signoff/                     ← one doc per VIP release
├── scripts/
│   ├── setup_env.sh
│   ├── clean.sh
│   └── report_gen.py
└── .github/
    └── workflows/
        └── dv_regression.yml
```

---

## Per-VIP Directory Structure

```
vip/<vip_name>/
│
├── README.md                    ← VIP user guide
├── CHANGELOG.md
│
├── rtl/                         ← DUT under test (for simulation)
│   └── <dut>.sv
│
├── uvm/
│   ├── transaction/
│   │   └── <vip>_seq_item.sv
│   ├── sequence/
│   │   ├── <vip>_base_seq.sv
│   │   ├── <vip>_write_seq.sv
│   │   ├── <vip>_read_seq.sv
│   │   ├── <vip>_random_seq.sv
│   │   ├── <vip>_burst_seq.sv
│   │   └── <vip>_error_seq.sv
│   ├── sequencer/
│   │   └── <vip>_sequencer.sv
│   ├── driver/
│   │   └── <vip>_driver.sv
│   ├── monitor/
│   │   └── <vip>_monitor.sv
│   ├── agent/
│   │   ├── <vip>_agent.sv
│   │   └── <vip>_agent_cfg.sv
│   ├── env/
│   │   ├── <vip>_env.sv
│   │   └── <vip>_env_cfg.sv
│   ├── scoreboard/
│   │   └── <vip>_scoreboard.sv
│   ├── predictor/
│   │   └── <vip>_predictor.sv
│   ├── coverage/
│   │   └── <vip>_coverage.sv
│   ├── assertions/
│   │   └── <vip>_assertions.sv
│   └── pkg/
│       └── <vip>_pkg.sv
│
├── tb/
│   ├── tb_top.sv
│   └── filelist.f
│
├── tests/
│   ├── <vip>_base_test.sv
│   ├── <vip>_smoke_test.sv
│   ├── <vip>_write_test.sv
│   ├── <vip>_read_test.sv
│   ├── <vip>_burst_test.sv
│   ├── <vip>_random_test.sv
│   ├── <vip>_ooo_test.sv
│   ├── <vip>_backpressure_test.sv
│   ├── <vip>_reset_test.sv
│   ├── <vip>_error_test.sv
│   ├── <vip>_stress_test.sv
│   └── <vip>_corner_test.sv
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── testplan.md
│
└── signoff/
    └── <vip>_signoff_v<N>.md
```

---

## VIP Scope — all protocols

The factory has **no restricted VIP list**. Every protocol in `vip-portfolio.md` is in scope —
USB, chiplet and bus, MIPI, automotive, memory, networking, SoC and avionics, PCIe and CXL, storage,
AMBA, display, RISC-V and others — along with any protocol not listed and any customer-proprietary
interface.

The lifecycle, regression tiers, PASS authority policy, skeleton and signoff artifacts below are
identical for every VIP regardless of protocol. Nothing in the flow is protocol-specific; only the
transaction fields, constraints, coverpoints and assertions are, and those are derived from the
protocol specification.

Sequence work by demand, not by a fixed roadmap. Record the current active set and priority order in
`/areas/vip-factory.md`, not in this document — a hardcoded roadmap goes stale and gets mistaken for
a limit.

## VIP Lifecycle (mandatory for every VIP)

```
GATE 0  — Requirements complete
GATE 1  — Architecture approved (VIP Architect sign-off)
GATE 2  — Compilation PASS (L0)
GATE 3  — Smoke PASS (L1: 100%)
GATE 4  — Directed feature tests PASS (L2: 100%)
GATE 5  — Random regression PASS (L3: ≥99%, 100 seeds)
GATE 6  — Negative tests PASS (expected violations caught)
GATE 7  — Assertions PASS (all exercised, none vacuous)
GATE 8  — Coverage closure (functional ≥95%, code ≥90%)
GATE 9  — Full regression PASS (L5: all tiers)
GATE 10 — Independent review complete
GATE 11 — SIGNOFF (version tagged in Git)
```

**Every gate has a documented artifact. No artifact = gate not passed.**
