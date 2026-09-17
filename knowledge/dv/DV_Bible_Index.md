# DV Engineering Bible Vol I — Chapter Index

> Source: *Design Verification Engineering Bible™ v1.0* by Avik Majumdar
> 47 chapters · 4 parts · ~282 pp

## Part I — Foundations (Ch 1–10)

| Ch | Title | Key Topics |
|---|---|---|
| 1 | What is Design Verification? | Philosophy, verification pyramid, cost of bugs, DV evolution |
| 2 | Digital Logic Fundamentals | Combinational/sequential, FSMs, pipelines, reset, CDC basics |
| 3 | Computer Architecture for DV | Memory hierarchy, caches, buses, pipeline hazards, interrupts |
| 4 | RTL Design Fundamentals | RTL coding style, synthesis awareness, latch inference, timing paths |
| 5 | Verification Methodology Overview | Directed → CRV → CDV → Formal → Hybrid → AI-assisted |
| 6 | SystemVerilog for Verification | Interfaces, clocking blocks, program blocks, data types, processes |
| 7 | Object-Oriented Programming in SV | Classes, inheritance, polymorphism, virtual methods, parameterization |
| 8 | UVM Architecture | Factory, config_db, phases, TLM ports, analysis ports, objections |
| 9 | Simulation Semantics | Delta cycles, race conditions, scheduler, stratified event queue |
| 10 | EDA Tool Ecosystem | VCS, Xcelium, Questa — compile/elab/sim flow, switches, waveform formats |

## Part II — Environment Engineering (Ch 11–25)

| Ch | Title | Key Topics |
|---|---|---|
| 11 | Verification Plan (Vplan) | Feature decomposition, scenario matrix, coverpoint mapping, traceability |
| 12 | Interface Design | Virtual interfaces, clocking blocks, modport, interface arrays |
| 13 | UVM Agent Architecture | Driver, monitor, sequencer, agent config, passive/active modes |
| 14 | UVM Environment Architecture | Env layering, multi-agent, scoreboard integration, top-level config |
| 15 | Sequence Architecture | sequence_item, base_seq, layered seqs, sequence libraries, p_sequencer |
| 16 | UVM Config & Factory | config_db patterns, type/instance overrides, `set_type_override_by_type` |
| 17 | Scoreboards & Reference Models | In-order/out-of-order, TLM analysis, expected vs. actual, error injection |
| 18 | Register Abstraction Layer (RAL) | uvm_reg, uvm_reg_block, frontdoor/backdoor, adapter, predictor |
| 19 | Protocol-Aware VIP Design | AXI/AHB/APB agent anatomy, protocol checker integration, VIP config |
| 20 | Clock Domain Crossing (CDC) | Synchronizers, metastability, CDC-aware assertion, tools (Spyglass/Meridian) |
| 21 | Reset Strategy Verification | Async/sync reset, partial reset, reset domain crossing, reset sequences |
| 22 | Memory Subsystem Verification | DRAM model, memory map, boundary conditions, ECC checking |
| 23 | Interrupt Verification | IRQ routing, priority, masking, software-visible registers, ISR sequences |
| 24 | DFT Verification | Scan insertion awareness, BIST, JTAG, at-speed test exclusion zones |
| 25 | Low-Power Verification (UPF) | Power domains, retention, isolation, supply sets, CPF/UPF-aware simulation |

## Part III — Stimulus, Coverage & Formal (Ch 26–36)

| Ch | Title | Key Topics |
|---|---|---|
| 26 | Constrained-Random Verification | `rand`/`randc`, constraints, `solve..before`, `constraint_mode`, `rand_mode` |
| 27 | Functional Coverage | Covergroups, coverpoints, bins, cross, `option.per_instance`, URG flow |
| 28 | Code Coverage | Line, statement, branch, condition, toggle, FSM — VCS `-cm` flags, exclusion |
| 29 | Assertion-Based Verification | `assert property`, `assume property`, `cover property`, vacuity, disable iff |
| 30 | SystemVerilog Assertions (SVA) | Sequences, temporal operators, `$past`/`$rose`/`$fell`, bind blocks |
| 31 | Formal Verification | Bounded model checking, induction, assume/assert, JasperGold / VC Formal |
| 32 | Coverage Closure | Hole classification, waivers, directed test generation, incremental regression |
| 33 | Negative Testing | Protocol violations, boundary injection, error recovery, illegal transactions |
| 34 | Power-Aware Simulation | Switching activity, dynamic power estimation, UPF/CPF simulation hooks |
| 35 | Performance Verification | Latency/BW/throughput measurement, performance scoreboards, traffic models |
| 36 | Security Verification | Trust zones, access control, secure boot, information leakage testing |

## Part IV — Professional Engineering (Ch 37–47)

| Ch | Title | Key Topics |
|---|---|---|
| 37 | Regression Infrastructure | Farm setup, Jenkins/LSF/Slurm, seed management, parallel dispatch |
| 38 | Debug Methodology | Log RCA, waveform navigation, delta-cycle debug, tool-specific tricks |
| 39 | Failure Analysis & Clustering | Auto-clustering, fingerprinting, historical comparison, flaky detection |
| 40 | Verification Reuse | IP-level → subsystem → SoC VIP promotion, parameterization, SVA portability |
| 41 | Agentic AI in DV | Multi-agent architecture, LLM+RAG, planner/test-gen/debug/closure agents |
| 42 | UVM Methodology Extensions | Register sequences, virtual sequences, layered protocol, response handling |
| 43 | NoC Verification | Multi-master/multi-slave, traffic matrix coverage, ordering, deadlock detection |
| 44 | High-Speed Interface DV | PCIe/DDR/CXL bring-up methodology, link training sequences, eye diagram hooks |
| 45 | Embedded SW Co-Verification | ISS integration, bare-metal tests, OS-aware sim, HW/SW handshake |
| 46 | Verification Architecture | Scalability patterns, env taxonomy, team DV org, reuse library governance |
| 47 | Metrics, Signoff & Tapeout | RTM, coverage metrics, regression health, VMM, risk-adjusted signoff |

## The AVIK Studio Golden Rules (from the Bible)

> "Never verify code. Verify behavior."

> "Verification is complete not when the simulation stops, but when the evidence is sufficient,
>  the risks are understood, the residuals are accepted, and the engineering team can stand behind
>  the decision."

## Verification Maturity Model (VMM) — Bible Ch 47

```
Level 1 — Ad Hoc:     Directed tests, no plan, no coverage
Level 2 — Defined:    Verification plan exists, basic coverage
Level 3 — Measured:   Coverage-driven, metrics tracked
Level 4 — Managed:    Risk-based, formal used, dashboards live
Level 5 — Optimized:  AI-assisted, continuous improvement, reuse library
```

Most industrial teams target Level 3–4. Avik's current dv_agentic work targets Level 4–5.
