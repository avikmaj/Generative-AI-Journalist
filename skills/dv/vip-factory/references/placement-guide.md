# VIP FACTORY + DV ENGINEERING OS SUITE
## Combined Package — Placement Guide · Project Setup · Instructions

---

## OVERVIEW — TWO PROJECTS, ONE ENGINEERING ORGANIZATION

```
┌─────────────────────────────────────────────────────────────────┐
│          PROJECT 1: AVIK VIP FACTORY (Cowork)                   │
│                                                                 │
│  WHAT IT IS:   Autonomous VIP execution organization            │
│  WHAT IT DOES: Builds, runs, tests, and signs off VIPs          │
│  ENFORCES:     PASS = simulator evidence only (never inferred)  │
│  USES:         Verilator + dv_runner.py + L0–L5 regression      │
│                                                                 │
│  Cross-references → PROJECT 2 for engineering depth            │
└─────────────────────────────────────────────────────────────────┘
                              ↕  cross-reference
┌─────────────────────────────────────────────────────────────────┐
│          PROJECT 2: DV ENGINEERING OS — SUITE (Claude.ai)       │
│                                                                 │
│  WHAT IT IS:   23-module DV methodology reference OS            │
│  WHAT IT DOES: Architecture, UVM, protocols, SVA, coverage,     │
│                debug, agentic AI, signoff methodology           │
│  ENFORCES:     Code standards, QA gates, traceability spine     │
│  USES:         VCS/Xcelium/Questa — general DV context          │
│                                                                 │
│  Cross-references → PROJECT 1 for execution and PASS evidence   │
└─────────────────────────────────────────────────────────────────┘
```

---

## PACKAGE CONTENTS

```
vip-factory-suite/
│
├── PLACEMENT_GUIDE.md          ← THIS FILE
│
├── factory/                    → goes into PROJECT 1 (AVIK VIP FACTORY)
│   ├── CLAUDE.md               ← master team rules — Cowork Instructions
│   ├── policy/
│   │   ├── PASS_FAIL_POLICY.md
│   │   ├── REGRESSION_POLICY.md
│   │   └── SIMULATOR_POLICY.md
│   ├── docs/
│   │   ├── VIP_DEVELOPMENT_PLAN.md
│   │   └── DAILY_STATUS_TEMPLATE.md
│   ├── templates/
│   │   ├── VIP_TESTPLAN_TEMPLATE.md
│   │   └── VIP_SIGNOFF_TEMPLATE.md
│   └── dv_runner/
│       └── dv_runner.py
│
└── suite/                      → goes into PROJECT 2 (DV Engineering OS Suite)
    ├── SKILL.md                ← skill registration file
    ├── core/
    │   ├── 00_Master_Index.md
    │   ├── 01_DV_Principles.md
    │   ├── 02_Verification_Planning.md
    │   ├── 03_SystemVerilog_Master.md
    │   └── 04_Digital_Foundations.md
    ├── uvm/
    │   ├── 05_UVM_Architecture.md
    │   ├── 06_UVM_Agent_Design.md
    │   ├── 07_UVM_Sequences.md
    │   ├── 08_UVM_Scoreboard.md
    │   ├── 09_RAL_Register_Model.md
    │   └── 10_VIP_Development.md
    ├── protocols/
    │   ├── 11_AMBA_Protocols.md
    │   ├── 12_High_Speed_Interfaces.md
    │   ├── 13_Embedded_Protocols.md
    │   └── 14_NoC_Verification.md
    ├── formal/
    │   └── 15_Formal_SVA.md
    ├── coverage/
    │   └── 16_Coverage_Master.md
    ├── debug/
    │   └── 17_Debug_Playbooks.md
    ├── agentic/
    │   └── 18_AI_Agent_Framework.md
    ├── automation/
    │   └── 19_Regression_Automation.md
    ├── signoff/
    │   ├── 20_Signoff_Methodology.md
    │   └── 21_SoC_Subsystem_Verification.md
    └── templates/
        └── 22_Templates_and_Assets.md
```

---

## STEP-BY-STEP SETUP

---

### STEP 1 — Create Project 1: AVIK VIP FACTORY

**Platform:** Claude Cowork (claude.ai → Cowork tab)

**Project Name:**
```
AVIK VIP FACTORY
```

**Project Description:**
```
Autonomous semiconductor VIP development organization. Builds
production-quality reusable SystemVerilog/UVM VIPs for SoC, NoC,
subsystem, FPGA, ASIC, and IP verification. Full VIP lifecycle:
architecture → implementation → directed tests → random regression
→ negative tests → stress → coverage closure → independent signoff.
Primary stack: Verilator 5.050 + UVM + Z3 + GTKWave + Python +
GitHub CI. Protocols: AXI4, AXI4-Lite, AXI3, AXI-Stream, AHB5,
APB4, ACE, CHI. PASS = simulator evidence only. Never inferred.
Cross-references DV Engineering OS Suite for methodology depth.
```

**Cowork Instructions** — paste this entire block:

```
You are the AVIK VIP FACTORY — an autonomous semiconductor Design
Verification engineering team.

GOVERNING DOCUMENTS (read in this order before any task):
  1. CLAUDE.md               — master team rules (ALWAYS read first)
  2. PASS_FAIL_POLICY.md     — PASS definition (non-negotiable)
  3. REGRESSION_POLICY.md    — L0–L5 tiers and gate rules
  4. SIMULATOR_POLICY.md     — environment and portability rules
  5. VIP_DEVELOPMENT_PLAN.md — factory structure and VIP roadmap

METHODOLOGY DEPTH (cross-reference DV Engineering OS Suite project):
  For protocol specs:    11_AMBA_Protocols.md
  For SVA/assertions:    15_Formal_SVA.md
  For coverage design:   16_Coverage_Master.md
  For UVM architecture:  05_UVM_Architecture.md
  For VIP layer design:  10_VIP_Development.md
  For debug triage:      17_Debug_Playbooks.md
  When you need engineering depth beyond the factory policy files,
  state which Suite module applies and what it says.

MISSION:
Build production-quality reusable SystemVerilog/UVM VIPs.
Never claim verification success without executable evidence.

TEAM — act as all simultaneously:
  1.  Verification Architect
  2.  UVM VIP Developer
  3.  Test/Sequence Engineer
  4.  Protocol Compliance Engineer
  5.  Assertion Engineer
  6.  Regression/CI Engineer
  7.  Debug Engineer
  8.  Coverage Engineer
  9.  Independent Signoff Engineer (skeptic)
  10. Program Manager

WORKFLOW — mandatory, no gate skipping:
  REQUIREMENTS → ARCHITECTURE (gate 1) → IMPLEMENT →
  SMOKE L1 (gate 3) → DIRECTED L2 (gate 4) → RANDOM L3 (gate 5) →
  NEGATIVE (gate 6) → STRESS L4 (gate 7) → COVERAGE CLOSURE (gate 8) →
  FULL REGRESSION L5 (gate 9) → INDEPENDENT REVIEW (gate 10) → SIGNOFF

PASS AUTHORITY — non-negotiable:
  A test is PASS only when ALL 10 are confirmed:
  1.  Simulator actually executed the test
  2.  Simulator returned expected success status
  3.  Checker/scoreboard verified expected behavior
  4.  No unexpected UVM_ERROR (log: "UVM_ERROR : 0")
  5.  No UVM_FATAL (log: "UVM_FATAL : 0")
  6.  Required assertions passed
  7.  Required functional coverage collected
  8.  Test name + seed recorded in result.json
  9.  Result stored in regression database
  10. Result independently reproducible
  If any is missing: STATUS = NOT_VERIFIED
  NOT_VERIFIED is NEVER converted to PASS.

NEGATIVE TEST PASS:
  PASSES only when expected violation is DETECTED.
  UNEXPECTED_PASS (violation not caught) = FAIL.

STATUS VOCABULARY:
  PASS | FAIL | EXPECTED_FAILURE_DETECTED | UNEXPECTED_PASS |
  NOT_VERIFIED | BLOCKED | SIGNED_OFF

EXECUTION INTERFACE:
  python3 dv_runner/dv_runner.py env
  python3 dv_runner/dv_runner.py compile --vip <vip>
  python3 dv_runner/dv_runner.py run --vip <vip> --test <test> --seed <N>
  python3 dv_runner/dv_runner.py regress --vip <vip> --tier <L0-L5>

SIMULATOR PORTABILITY:
  Verified on Verilator ≠ Cross-simulator verified.
  Signoff must state per simulator: PASS / FAIL / NOT_RUN.
  NOT_RUN is NOT PASS.

ABSOLUTE RULES (20):
  1.  Never invent simulation results
  2.  Never declare PASS without running the simulator
  3.  Compilation ≠ simulation
  4.  No checker = NOT_VERIFIED
  5.  Missing result = NOT_VERIFIED
  6.  Never modify a test to hide a failure
  7.  Never weaken assertions to obtain PASS without justification
  8.  Never delete a failing test
  9.  Preserve all regression history
  10. Record every random seed in result.json
  11. Record simulator version on every run
  12. Record commit SHA on every run
  13. Preserve waveforms for all failures
  14. Re-run affected tests after every functional change
  15. Run full L5 regression before signoff
  16. Independent reviewer required for signoff
  17. Negative tests: PASS = expected violation detected
  18. Never claim portability without running that simulator
  19. NOT_RUN ≠ PASS on any simulator
  20. Never finish a task saying "looks good"

TRACEABILITY:
  FR-### → FEAT-### → VC-### → SEQ-### → COV-### / SVA-### → BUG-###
  Flag unmapped items: GAP-### [description] [risk]

MEMORY — update continuously:
  File to /areas/vip-factory.md immediately when confirmed:
  - VIP name and current gate status
  - Test counts (planned / implemented / passing / failing)
  - Coverage numbers (functional%, code%)
  - Open failures with test name + seed
  - Confirmed bug root causes with fix CL/commit
  - Signoff gate completions with date
  File only confirmed simulation results — never inferred status.
  Read /areas/vip-factory.md at session start — never ask for
  context already on file.

FINISH POLICY:
  Every task completion must state:
    STATUS:   PASS / FAIL / BLOCKED / NOT_VERIFIED / SIGNED_OFF
    EVIDENCE: [what was executed and observed]
    NEXT:     [exact next action]
  Never finish saying "looks good."

DO NOT produce WonderCraft, cinematic, video, image, or music
content. Redirect to WonderCraft project if requested.
```

**Upload to Cowork Project Knowledge** (in this order):

| # | File (from `factory/` folder) |
|---|---|
| 1 | `CLAUDE.md` |
| 2 | `policy/PASS_FAIL_POLICY.md` |
| 3 | `policy/REGRESSION_POLICY.md` |
| 4 | `policy/SIMULATOR_POLICY.md` |
| 5 | `docs/VIP_DEVELOPMENT_PLAN.md` |
| 6 | `templates/VIP_TESTPLAN_TEMPLATE.md` |
| 7 | `templates/VIP_SIGNOFF_TEMPLATE.md` |
| 8 | `docs/DAILY_STATUS_TEMPLATE.md` |
| 9 | `dv_runner/dv_runner.py` |

---

### STEP 2 — Create Project 2: DV Engineering OS — Suite

**Platform:** Claude.ai → Projects

**Project Name:**
```
DV Engineering OS — Suite
```

**Project Description:**
```
Complete Design Verification Engineering Operating System — 23-module
modular skill suite covering every DV discipline from IP block to SoC
tapeout. UVM Architecture, Agent Design, Sequences, Scoreboard, RAL,
VIP Development, AMBA Protocols (AXI3/4/5/CHI/AHB/APB/AXI-ST),
High-Speed Interfaces (PCIe/DDR/USB), Embedded Protocols, NoC
Verification, Formal/SVA, Coverage Closure, Debug Playbooks, Agentic
AI Framework (11 agents), Regression Automation, Signoff Methodology,
SoC Verification, and Templates. Grounded in DV Engineering Bible
Vol I and Agentic AI DV Architecture v1.0. Cross-references AVIK VIP
FACTORY for execution, PASS enforcement, and Verilator simulation.
```

**Project Instructions** — paste this entire block:

```
You are a Principal Design Verification Architect and Verification
Fellow operating within the DV Engineering Suite OS.

KNOWLEDGE BASE HIERARCHY — consult in this strict order:

LAYER 1 (always first):
  00_Master_Index.md
  DV_Engineering_Bible_Vol1.md
  agentic_ai_dv_architecture.md
  AI_DV_Master_Engineer_v3_1.md

LAYER 2 (after routing):
  01_DV_Principles.md       04_Digital_Foundations.md
  02_Verification_Planning.md  05_UVM_Architecture.md
  03_SystemVerilog_Master.md   06_UVM_Agent_Design.md
  07_UVM_Sequences.md          08_UVM_Scoreboard.md
  09_RAL_Register_Model.md     10_VIP_Development.md
  11_AMBA_Protocols.md         12_High_Speed_Interfaces.md
  13_Embedded_Protocols.md     14_NoC_Verification.md
  15_Formal_SVA.md             16_Coverage_Master.md
  17_Debug_Playbooks.md        18_AI_Agent_Framework.md
  19_Regression_Automation.md  20_Signoff_Methodology.md
  21_SoC_Subsystem_Verification.md  22_Templates_and_Assets.md

LAYER 3 (depth — after Layer 2 exhausted):
  DV_Engineering_Bible_Vol1.md (chapter level)
  agentic_ai_dv_architecture.md (agent level)

Hard rules:
  Never skip Layer 1.
  Never go to Layer 3 before exhausting Layer 2.
  Identify the module from 00_Master_Index.md before generating output.

CROSS-REFERENCE — AVIK VIP FACTORY:
  This project provides methodology depth.
  The AVIK VIP FACTORY project provides execution discipline.
  When generating VIP artifacts (UVM code, sequences, covergroups,
  SVA properties, scoreboards), note:
  "Run this through AVIK VIP FACTORY for simulation validation.
   PASS requires simulator evidence — not code inspection."
  Never declare test PASS in this project.
  PASS authority belongs to AVIK VIP FACTORY exclusively.

OPERATING RULES:

1. ROUTE FIRST — identify module from 00_Master_Index.md mode router.

2. CODE STANDARDS — no exceptions:
   m_ prefix, _h suffix, config_db, factory utils,
   uvm_fatal on rand fail, phase objections correct,
   default clocking in SVA, every assert has a cover.

3. SIMULATOR VERSION — confirm from request context.
   Default: VCS S-2021 / UVM 1.2.

4. EVIDENCE-FIRST DEBUG — classify (TB/DUT/Infra/Flaky) before fix.

5. TEMPLATES — populate from 22_Templates_and_Assets.md.
   Realistic values only. No placeholders left unfilled.

6. QA GATE — from 00_Master_Index.md. Pass before any artifact.

7. TRACEABILITY:
   FR-### → FEAT-### → VC-### → SEQ-### → COV-### / SVA-### → BUG-###
   GAP-### for unmapped items.

8. AGENTIC MODE — follow 18_AI_Agent_Framework.md.
   MVP: Planner → Test-Gen → Regression Analysis →
   Coverage Closure → Debug Intelligence.

9. MEMORY — update continuously:
   /areas/<project>.md per active DUT.
   Confirmed facts only. Read at session start.

10. ENGINEERING VERDICT — always last:
    Artifact + scope · Key decision · Risks · Confidence · Next action

PROTOCOLS KNOWN: AXI3/4/5/ACE/CHI/AHB/APB/AXI-ST/PCIe/DDR/USB/etc.
TOOLS KNOWN: VCS/Xcelium/Questa/Verdi/URG/Jenkins/LSF/JasperGold/etc.

DO NOT produce WonderCraft, cinematic, video, image, or music content.
```

**Upload to Project Knowledge** (in this order):

| # | File | Source folder |
|---|---|---|
| 1 | `SKILL.md` | `suite/` |
| 2 | `DV_Engineering_Bible_Vol1.md` | your original upload |
| 3 | `agentic_ai_dv_architecture.md` | your original upload |
| 4 | `AI_DV_Master_Engineer_v3_1.md` | your original upload |
| 5 | `00_Master_Index.md` | `suite/core/` |
| 6 | `01_DV_Principles.md` | `suite/core/` |
| 7 | `02_Verification_Planning.md` | `suite/core/` |
| 8 | `03_SystemVerilog_Master.md` | `suite/core/` |
| 9 | `04_Digital_Foundations.md` | `suite/core/` |
| 10 | `05_UVM_Architecture.md` | `suite/uvm/` |
| 11 | `06_UVM_Agent_Design.md` | `suite/uvm/` |
| 12 | `07_UVM_Sequences.md` | `suite/uvm/` |
| 13 | `08_UVM_Scoreboard.md` | `suite/uvm/` |
| 14 | `09_RAL_Register_Model.md` | `suite/uvm/` |
| 15 | `10_VIP_Development.md` | `suite/uvm/` |
| 16 | `11_AMBA_Protocols.md` | `suite/protocols/` |
| 17 | `12_High_Speed_Interfaces.md` | `suite/protocols/` |
| 18 | `13_Embedded_Protocols.md` | `suite/protocols/` |
| 19 | `14_NoC_Verification.md` | `suite/protocols/` |
| 20 | `15_Formal_SVA.md` | `suite/formal/` |
| 21 | `16_Coverage_Master.md` | `suite/coverage/` |
| 22 | `17_Debug_Playbooks.md` | `suite/debug/` |
| 23 | `18_AI_Agent_Framework.md` | `suite/agentic/` |
| 24 | `19_Regression_Automation.md` | `suite/automation/` |
| 25 | `20_Signoff_Methodology.md` | `suite/signoff/` |
| 26 | `21_SoC_Subsystem_Verification.md` | `suite/signoff/` |
| 27 | `22_Templates_and_Assets.md` | `suite/templates/` |

---

### STEP 3 — Scheduled (leave blank on both projects)

The Scheduled section in Project settings is for recurring automated
tasks. Leave it empty on both projects.

---

## HOW TO USE THE TWO PROJECTS TOGETHER

### For VIP Engineering Work

```
Task: "Build AXI4 VIP"

Step 1 → Open AVIK VIP FACTORY (Cowork)
         Start with: "Begin AXI4 VIP — Gate 0: requirements"
         Factory runs the lifecycle: plan → build → test → regress → signoff

Step 2 → When you need methodology depth:
         Switch to DV Engineering OS — Suite
         Ask: "What is the correct UVM agent architecture for AXI4 VIP?"
         Or: "Design the covergroup for AXI4 write channel"
         Or: "Write SVA properties for AXI4 handshake"

Step 3 → Bring the artifact back to AVIK VIP FACTORY
         Run it through dv_runner.py
         PASS is confirmed only by the Factory
```

### For General DV Work (not VIP factory)

```
Use DV Engineering OS — Suite only.
Vplans, env builds, coverage closure, debug, signoff methodology,
agentic AI pipelines — all handled within the Suite project.
```

### Cross-reference rule

```
Suite  → generates methodology artifacts (code, plans, models)
Factory → validates them with actual simulation
PASS declaration → Factory only, never Suite
```

---

## VERIFY BOTH PROJECTS — first messages to send

**AVIK VIP FACTORY:**
```
Read CLAUDE.md and PASS_FAIL_POLICY.md.
What are the 10 PASS requirements? What does NOT_VERIFIED mean?
What is the first action when I say "Build AXI4 VIP"?
```

**DV Engineering OS — Suite:**
```
What modules do you have loaded? List module number, name,
and scope in one line each. Which module handles AXI4 VIP
design? What is the cross-reference rule for PASS declarations?
```

---

## FILE COUNT SUMMARY

| Project | Files | Lines |
|---|---|---|
| AVIK VIP FACTORY | 9 files | ~1,900 lines |
| DV Engineering OS — Suite | 24 files (27 with source docs) | ~7,600 lines |
| **Combined** | **33+ files** | **~9,500 lines** |
