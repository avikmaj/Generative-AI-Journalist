---
name: dv-engineering-suite
description: >-
  DV Engineering OS — complete 23-module verification suite for ASIC/SoC/FPGA/IP.
  Use WHENEVER: vplan/RTM/traceability; UVM env/agent/seq/scoreboard/RAL/VIP;
  SVA/formal; AMBA protocols (AXI3/4/5/CHI/AHB/APB/AXI-ST); PCIe/DDR/USB/NoC;
  coverage closure (functional/code/toggle/FSM/assertion); regression triage/clustering;
  agentic AI DV workflows (15 specialists plus orchestrator); signoff evidence packages;
  SoC/subsystem verification; debug playbooks. Grounded in DV Engineering Bible Vol I
  and SUPER-BRAIN DV Architecture v2.0. Triggered by any DV engineering keyword.
  DO NOT use for cinematic/video/image/music content — that is the genai family.
---

# DV Engineering OS — Complete Suite

> *"Design creates hardware. Verification creates confidence."* — DV Engineering Bible Vol I
> *"Never verify code. Verify behavior."* — Golden Rule

This skill routes every DV engineering request to the correct specialist module. Read
[the master index](references/core/00_Master_Index.md) for the full mode router, operating
philosophy, abstraction coverage and traceability spine. The module filenames in the router below
resolve through that index.

For coordinated multi-agent work, read [module 18](references/agentic/18_AI_Agent_Framework.md) and
the SUPER-BRAIN DV architecture in `knowledge/dv/agentic_ai_dv_architecture.md`. Activate only the
roles a concrete task needs. Dispatch real workers when delegation is available and authorized, and
preserve independent review by worker identity. Run debug/retest and coverage/retest loops with
evidence tied to the current source and configuration. An independent review PASS authorises only the
explicitly reviewed advancement; the orchestrator owns readiness, and the human engineering authority
owns final signoff and waivers.

Deeper methodology lives outside the skill, in `knowledge/dv/`:
`DV_Engineering_Bible_Vol1.md` (47 chapters, indexed by `DV_Bible_Index.md`) and
`AI_DV_Master_Engineer_v3_1.md` (architect persona and response format). Read those only when a
module is insufficient — they are large.

## Module router

| Task keyword | Module | File |
|---|---|---|
| principles / methodology / CDV / pyramid | 01 | `references/core/01_DV_Principles.md` |
| vplan / requirements / traceability / feature | 02 | `references/core/02_Verification_Planning.md` |
| SystemVerilog / interface / clocking / data type | 03 | `references/core/03_SystemVerilog_Master.md` |
| FSM / CDC / RDC / pipeline / timing / reset | 04 | `references/core/04_Digital_Foundations.md` |
| UVM / factory / phase / config_db / TLM | 05 | `references/uvm/05_UVM_Architecture.md` |
| agent / driver / monitor / sequencer | 06 | `references/uvm/06_UVM_Agent_Design.md` |
| sequence / constraint / stimulus / virtual seq | 07 | `references/uvm/07_UVM_Sequences.md` |
| scoreboard / predictor / reference model | 08 | `references/uvm/08_UVM_Scoreboard.md` |
| RAL / register / frontdoor / backdoor | 09 | `references/uvm/09_RAL_Register_Model.md` |
| VIP / BFM / protocol agent design | 10 | `references/uvm/10_VIP_Development.md` |
| AXI / AHB / APB / CHI / ACE / AXI-ST | 11 | `references/protocols/11_AMBA_Protocols.md` |
| PCIe / CXL / UCIe / DDR / USB / Ethernet | 12 | `references/protocols/12_High_Speed_Interfaces.md` |
| SPI / I2C / I3C / UART / CAN / MIPI / JTAG | 13 | `references/protocols/13_Embedded_Protocols.md` |
| NoC / interconnect / traffic / deadlock | 14 | `references/protocols/14_NoC_Verification.md` |
| SVA / formal / property / assume / assert | 15 | `references/formal/15_Formal_SVA.md` |
| coverage / covergroup / URG / hole / closure | 16 | `references/coverage/16_Coverage_Master.md` |
| debug / log / waveform / RCA / cluster / flaky | 17 | `references/debug/17_Debug_Playbooks.md` |
| agentic / AI agent / LLM / RAG / pipeline | 18 | `references/agentic/18_AI_Agent_Framework.md` |
| regression / Jenkins / LSF / farm / CI/CD | 19 | `references/automation/19_Regression_Automation.md` |
| signoff / tapeout / evidence / milestone | 20 | `references/signoff/20_Signoff_Methodology.md` |
| SoC / subsystem / full-chip / performance | 21 | `references/signoff/21_SoC_Subsystem_Verification.md` |
| template / scaffold / fill-in / YAML | 22 | `references/templates/22_Templates_and_Assets.md` |

When a request spans modules, lock the spec and feature context first, then run each module in
dependency order.

## Fill-in scaffolds

Use these directly rather than inventing a shape:

| Asset | Use for |
|---|---|
| `assets/vplan_template.yaml` | Verification plan with requirement-to-coverage mapping |
| `assets/uvm_env_template.sv` | UVM environment skeleton following the code standards below |
| `assets/agent_pipeline_schema.yaml` | Agentic DV pipeline role and dispatch definition |
| `assets/signoff_package.yaml` | Signoff evidence package structure |

## Code standards (always active)

Apply these to all SV/UVM implementations. For framework documentation, non-UVM directed
reproducers, or unavailable tools, record applicability and evidence gaps instead of claiming the
whole UVM/SVA gate was executed. A bounded single-seed reproducer may establish a defect; it cannot
establish regression stability or full feature closure.

- Member prefix `m_` · handle suffix `_h`
- `uvm_config_db` for all interface and config passing — never direct assignment
- `uvm_component_utils` / `uvm_object_utils` on every class
- `uvm_fatal` on every failed `randomize()` — never silent
- Phase objections raised before stimulus, dropped after drain
- SVA: `default clocking` always declared; every `assert` has a matching `cover`

## Universal QA gate — pass before presenting any artifact

- [ ] Specification requirement mapped — no free-floating tests
- [ ] Simulator and UVM version confirmed
- [ ] Code standards applied
- [ ] Coverage point defined for every feature tested
- [ ] SVA guard defined for every protocol invariant exercised
- [ ] Root cause classified (TB / DUT / Infra / Flaky) before any fix is proposed
- [ ] Waivers documented with justification before any hole is excluded
- [ ] Signoff evidence item identified for every delivered artifact
- [ ] Engineering Verdict delivered

## Traceability spine

Every object gets an ID:

```
FR-###   Feature Requirement (from spec)
  → FEAT-### Verification Feature (from vplan)
    → VC-###   Verification Component (env/agent/scoreboard)
      → SEQ-###  Sequence / Test
        → COV-### Coverage Point · SVA-### Property
          → BUG-### Bug Report
            → AGT-### AI Agent (agentic pipeline)
```

Flag unmapped items as `GAP-### [description] [risk: LOW/MED/HIGH]`.

## Anti-patterns — never do these

| Anti-pattern | Consequence |
|---|---|
| Verify code, not behavior | Miss architecture-level bugs |
| Hardcode addresses in tests | Tests break on RTL changes |
| Self-checking by the driver | Correlation between stimulus and checker |
| Single-seed regression | False confidence in pass rate |
| Coverage without vplan traceability | Unknown what the coverage means |
| Waive holes without justification | Silent risk acceptance |
| Sign off on a coverage number alone | Residual risks unquantified |
| Blame the DUT before ruling out the TB | Wasted RTL debug time |
| Edit generated files instead of templates | Regeneration destroys the change |
| Commit without regression | Broken baseline not caught |

## Engineering Verdict format

Every response from this skill ends with:

```
VERDICT:
  Artifact:      [type + scope]
  Key decision:  [the most important engineering choice made]
  Risks/Open:    [what remains unresolved]
  Confidence:    [High/Med/Low — with the reason]
  Next action:   [the one thing to do next]
```
