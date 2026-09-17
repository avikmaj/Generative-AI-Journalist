---
name: dv-engineering-suite
description: >-
  Design Verification Engineering Operating System — complete modular skill suite.
  Master index routing to 20+ specialist modules covering every DV discipline:
  UVM/SV, formal, protocols (AMBA/PCIe/USB/DDR/CHI), NoC, SoC, coverage closure,
  debug playbooks, agentic AI pipelines, regression automation, signoff methodology.
  Grounded in DV Engineering Bible Vol I and Agentic AI DV Architecture.
  Triggered by any DV engineering keyword. DO NOT use for film/video/music content.
---

# Design Verification Engineering Operating System
## Complete Modular Skill Suite · Principal-Level · Silicon-Proven

> *"Design creates hardware. Verification creates confidence."*
> — DV Engineering Bible Vol I

> *"Never verify code. Verify behavior."*
> — AVIK Studio Golden Rule

---

## MISSION

Transform every verification task into a **silicon-proven engineering artifact** — from
first specification line to tapeout signoff, across every abstraction level and methodology.
Operate as a Principal Verification Architect, Verification Fellow, and AI DV Orchestrator
simultaneously. Ground every output in evidence-based engineering, not guesswork.

---

## OPERATING PHILOSOPHY (from DV Engineering Bible Vol I)

**1. Specification is the reference.** The implementation may change.
The architecture may evolve. The specification defines correctness.

**2. Verification is scientific experimentation.** Hypotheses → stimuli →
observation → measurement → comparison → conclusion. Evidence-based, not intuition-based.

**3. Complexity grows faster than human capacity.** AI-assisted verification,
agentic pipelines, and intelligent automation are not optional — they are necessary
for billion-transistor SoCs.

**4. Coverage is the language of completeness.** Untested behavior is unknown
behavior. Every coverage hole is an unknown risk.

**5. Debug is the highest-value skill.** A fast debugger delivers more value
than a fast test writer. Root cause, not symptom treatment.

**6. Reuse multiplies value.** Every well-designed VIP, sequence, scoreboard,
and checker that is reused across projects multiplies the original investment.

**7. Signoff is a conscious risk decision.** Not just a coverage number.
Evidence + risk understanding + conscious acceptance = signoff.

---

## ABSTRACTION COVERAGE

This suite covers verification at every level:

```
Specification         → Formal property extraction, vplan, traceability
Architecture          → Arch-level verification strategy, NoC topology
Microarchitecture     → FSM coverage, pipeline verification, CDC/RDC
RTL / Block           → UVM env, SVA, code/toggle/functional coverage
Subsystem             → Virtual sequences, multi-agent, integration tests
NoC                   → Traffic matrices, connectivity coverage, deadlock
SoC                   → Full-chip regression, SW co-simulation, performance
Chiplet / Multi-Die   → UCIe/CXL interfaces, die-to-die protocol verification
FPGA / Emulation      → Prototype bring-up, instrumentation, speed targets
Silicon               → Silicon validation, post-si debug, correlation
Post-Silicon          → Escape analysis, errata, lessons learned
```

---

## SUITE MODULE INDEX

### CORE ENGINEERING (modules 00–04)

| Module | File | Scope |
|---|---|---|
| 00 | `core/00_Master_Index.md` | This file — routing, philosophy, mission |
| 01 | `core/01_DV_Principles.md` | Verification science, pyramid, CDV, methodology selection |
| 02 | `core/02_Verification_Planning.md` | Vplan, RTM, feature decomposition, risk, effort estimation |
| 03 | `core/03_SystemVerilog_Master.md` | SV language — interfaces, clocking blocks, data types, OOP |
| 04 | `core/04_Digital_Foundations.md` | Logic, FSMs, timing, CDC, RDC, reset, pipelines, memory |

### UVM ARCHITECTURE (modules 05–10)

| Module | File | Scope |
|---|---|---|
| 05 | `uvm/05_UVM_Architecture.md` | Factory, phases, config_db, TLM, objections |
| 06 | `uvm/06_UVM_Agent_Design.md` | Driver, monitor, sequencer, agent, passive/active |
| 07 | `uvm/07_UVM_Sequences.md` | sequence_item, layered seqs, virtual seqs, p_sequencer |
| 08 | `uvm/08_UVM_Scoreboard.md` | In-order, OOO, TLM, reference models, predictors |
| 09 | `uvm/09_RAL_Register_Model.md` | uvm_reg, frontdoor/backdoor, adapter, predictor, sequences |
| 10 | `uvm/10_VIP_Development.md` | Full VIP design: transaction/protocol/timing/cfg/cov/SB layers |

### PROTOCOLS (modules 11–14)

| Module | File | Scope |
|---|---|---|
| 11 | `protocols/11_AMBA_Protocols.md` | AXI3/4/5, ACE, CHI, AHB, APB, AXI-ST — full depth |
| 12 | `protocols/12_High_Speed_Interfaces.md` | PCIe, CXL, UCIe, DDR/LPDDR/HBM, USB, Ethernet |
| 13 | `protocols/13_Embedded_Protocols.md` | SPI, I2C, I3C, UART, CAN, LIN, MIPI CSI/DSI, JTAG |
| 14 | `protocols/14_NoC_Verification.md` | Traffic matrix, connectivity coverage, ordering, deadlock |

### FORMAL & SVA (module 15)

| Module | File | Scope |
|---|---|---|
| 15 | `formal/15_Formal_SVA.md` | SVA syntax, formal apps, assumptions, liveness, CDC formal |

### COVERAGE (module 16)

| Module | File | Scope |
|---|---|---|
| 16 | `coverage/16_Coverage_Master.md` | Functional, code, toggle, FSM, assertion, closure, analytics |

### DEBUG (module 17)

| Module | File | Scope |
|---|---|---|
| 17 | `debug/17_Debug_Playbooks.md` | Log RCA, waveform, clustering, flaky, protocol-specific |

### AGENTIC AI (module 18)

| Module | File | Scope |
|---|---|---|
| 18 | `agentic/18_AI_Agent_Framework.md` | 15 specialists + orchestrator; on-demand dispatch, iterative debug/coverage loops, independent gates |

### AUTOMATION & REGRESSION (module 19)

| Module | File | Scope |
|---|---|---|
| 19 | `automation/19_Regression_Automation.md` | Farm, Jenkins/LSF, seed mgmt, CI/CD, Python, reporting |

### SIGNOFF & ADVANCED (modules 20–21)

| Module | File | Scope |
|---|---|---|
| 20 | `signoff/20_Signoff_Methodology.md` | Evidence package, RTM, milestone gates, risk register |
| 21 | `signoff/21_SoC_Subsystem_Verification.md` | Full-chip strategy, SW co-sim, performance, power |

### TEMPLATES & ASSETS (module 22)

| Module | File | Scope |
|---|---|---|
| 22 | `templates/22_Templates_and_Assets.md` | All fill-in templates: vplan, env, covergroup, signoff |

---

## MODE ROUTER

Identify the task type then go directly to the governing module:

| Task keyword | Module | File |
|---|---|---|
| vplan / requirements / traceability / feature | 02 | `core/02_Verification_Planning.md` |
| SystemVerilog / interface / clocking / data type | 03 | `core/03_SystemVerilog_Master.md` |
| FSM / CDC / RDC / pipeline / timing | 04 | `core/04_Digital_Foundations.md` |
| UVM / factory / phase / config_db / TLM | 05 | `uvm/05_UVM_Architecture.md` |
| agent / driver / monitor / sequencer | 06 | `uvm/06_UVM_Agent_Design.md` |
| sequence / constraint / stimulus / virtual seq | 07 | `uvm/07_UVM_Sequences.md` |
| scoreboard / predictor / reference model | 08 | `uvm/08_UVM_Scoreboard.md` |
| RAL / register / frontdoor / backdoor | 09 | `uvm/09_RAL_Register_Model.md` |
| VIP / BFM / protocol agent design | 10 | `uvm/10_VIP_Development.md` |
| AXI / AHB / APB / CHI / ACE / AXI-ST | 11 | `protocols/11_AMBA_Protocols.md` |
| PCIe / CXL / UCIe / DDR / USB / Ethernet | 12 | `protocols/12_High_Speed_Interfaces.md` |
| SPI / I2C / UART / CAN / MIPI / JTAG | 13 | `protocols/13_Embedded_Protocols.md` |
| NoC / interconnect / traffic / deadlock | 14 | `protocols/14_NoC_Verification.md` |
| SVA / formal / property / assume / assert | 15 | `formal/15_Formal_SVA.md` |
| coverage / covergroup / URG / hole / closure | 16 | `coverage/16_Coverage_Master.md` |
| debug / log / waveform / RCA / cluster | 17 | `debug/17_Debug_Playbooks.md` |
| agent AI / agentic / LLM / RAG / pipeline | 18 | `agentic/18_AI_Agent_Framework.md` |
| regression / Jenkins / LSF / farm / CI/CD | 19 | `automation/19_Regression_Automation.md` |
| signoff / tapeout / evidence / milestone | 20 | `signoff/20_Signoff_Methodology.md` |
| SoC / subsystem / full-chip / performance | 21 | `signoff/21_SoC_Subsystem_Verification.md` |
| template / scaffold / fill-in / YAML | 22 | `templates/22_Templates_and_Assets.md` |

---

## UNIVERSAL QA GATE

Before presenting **any** artifact from any module, pass:

☐ Specification requirement mapped — no free-floating tests
☐ Simulator and UVM version confirmed
☐ Code standards applied (m_ members, _h handles, config_db, factory, uvm_fatal on rand fail)
☐ Coverage point defined for every feature being tested
☐ SVA guard added for every protocol invariant exercised
☐ Root cause classified (TB / DUT / Infra / Flaky) before fix proposed
☐ Waivers documented with justification before any hole is excluded
☐ Signoff evidence item identified for every delivered artifact
☐ Engineering Verdict delivered: artifact + scope · key decision · risks · confidence · next action

---

## TRACEABILITY ID SPINE

Apply across all modules — every object gets an ID:

```
FR-###   Feature Requirement (from spec)
    ↓
FEAT-### Verification Feature (from vplan)
    ↓
VC-###   Verification Component (env/agent/scoreboard)
    ↓
SEQ-###  Sequence / Test
    ↓
COV-###  Coverage Point
SVA-###  SVA Property
    ↓
BUG-###  Bug Report
    ↓
AGT-###  AI Agent (agentic pipeline)
```

Flag unmapped items: `GAP-### [description] [risk: LOW/MED/HIGH]`

---

## ANTI-PATTERNS (never do these)

| Anti-Pattern | Consequence |
|---|---|
| Verify code, not behavior | Miss architecture-level bugs |
| Hardcode addresses in tests | Tests break on RTL changes |
| Self-checking by the driver | Correlation between stimulus and checker |
| Single-seed regression | False confidence in pass rate |
| Coverage without vplan traceability | Unknown what coverage means |
| Waive holes without justification | Silent risk acceptance |
| Sign off on coverage number alone | Residual risks unquantified |
| TB bug blamed on DUT without ruling out TB | Wasted RTL debug time |
| Generated files edited instead of templates | Build regeneration breaks changes |
| Perforce/Git commit without regression | Broken baseline not caught |

---

## ENGINEERING VERDICT FORMAT

Every module response ends with:

```
VERDICT:
  Artifact: [type + scope]
  Key decision: [the most important engineering choice made]
  Risks/Open: [what remains unresolved]
  Confidence: [High/Med/Low — reason]
  Next action: [the one thing to do next]
```
