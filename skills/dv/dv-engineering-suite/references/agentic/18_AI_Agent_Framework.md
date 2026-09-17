# Module 18 — Agentic AI DV Framework
## 11-Agent Architecture · RAG · LLM Prompt Patterns · MVP Rollout

> Source: Agentic AI Architecture for Pre-Silicon Design Verification v1.0

---

## 18.1 Why Agentic DV?

Modern DV generates massive disconnected artifacts — specs, vplans, UVM environments,
regression logs, coverage databases, waveforms, bug reports, dashboards.

An agentic AI architecture stitches these into an autonomous verification ecosystem where
specialized agents collaborate throughout the DV lifecycle: **planning, executing,
analyzing, and optimizing — continuously**.

The fundamental problem agentic DV solves:
```
Human capacity  ────────────────────────────── flat (linear with headcount)
Design complexity ──────────────────────────── exponential (node, feature growth)
Verification gap ══════════════════════════════ growing every generation
Agentic AI ═══════════════════════════════════ closes the gap
```

---

## 18.2 High-Level Agent Architecture

```
┌─────────────────────────────────────────────┐
│         DV Lead Agent (Orchestrator)        │
│  Goal Planning · Prioritization             │
│  Progress Tracking · Exit Criteria          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Verification Planner Agent             │
│  Spec Parsing · Req Extraction              │
│  Vplan Generation · Coverage Reqs           │
└──────┬───────────────────┬──────────────────┘
       │                   │
┌──────▼──────┐     ┌──────▼───────────────────┐
│ Test Gen    │     │  Coverage Analysis Agent  │
│ Agent       │     │  Func/Code/Toggle/Assert  │
│ UVM Seq     │     │  Hole Detection · Trends  │
└──────┬──────┘     └────────────┬──────────────┘
       └──────────────┬──────────┘
                      │
┌─────────────────────▼──────────────────────┐
│      Simulation Control Agent              │
│  Regression Sched · Farm Mgmt             │
│  Jenkins · LSF/Slurm · Log Collect        │
└─────────────────────┬──────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│      Debug Intelligence Agent             │
│  UVM Log Parse · RCA · Clustering         │
│  Waveform Hints · Bug Correlation         │
└─────────────────────┬──────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│      Coverage Closure Agent               │
│  Gap Analysis · Directed Test Gen         │
│  Constraint Recs · Regr Priority          │
└─────────────────────┬──────────────────────┘
                      │
┌─────────────────────▼──────────────────────┐
│      DV Dashboard Agent                   │
│  Coverage · Milestones · Bug Trends       │
│  Regression Health · Signoff Ready        │
└────────────────────────────────────────────┘
```

---

## 18.3 Agent Catalog — Full Specifications

### Agent 1 — Verification Planner

**Purpose:** Convert specs into a complete, structured verification plan.

**Inputs:**
- Architecture specification (PDF, MD, or text)
- Microarchitecture document
- Jira/GitHub feature list
- Confluence requirement pages
- Previous vplan (for incremental)

**LLM Prompt Pattern:**
```
SYSTEM:
You are a Principal DV Architect. Given the spec excerpt below,
extract all verifiable features and generate a vplan YAML conforming
exactly to this schema: {vplan_schema}
Return ONLY valid YAML. No prose, no markdown fences, no explanation.

USER:
Spec excerpt: {spec_text}
Protocol context: {protocol}
DUT name: {dut_name}
Previously extracted features (avoid duplicates): {existing_features}
```

**Output Schema:**
```yaml
feature:
  id: F###
  name: <name>
  priority: P0|P1|P2
  spec_ref: <section>
  risk: HIGH|MEDIUM|LOW
  scenarios:
    - id: F###_S##
      name: <name>
      stimulus: constrained_random|directed|formal
      coverage: [{covergroup, coverpoint, bins}]
      assertions: [<sva_name>]
```

---

### Agent 2 — Test Generation

**Purpose:** Synthesize UVM sequences targeting specific coverage gaps.

**Input Schema:**
```yaml
gap:
  feature: AXI Write Channel
  covergroup: axi_write_cg
  coverpoint: cp_awburst
  bin: WRAP
  uncovered_combinations:
    - awburst: WRAP
      awlen: 255
      awsize: 64B
```

**LLM Prompt Pattern:**
```
SYSTEM:
You are a UVM expert. Generate a complete UVM sequence targeting
the coverage gap below. Follow these standards exactly:
- m_ prefix for members, _h suffix for handles
- uvm_fatal on randomization failure (never silent fail)
- uvm_object_utils registration required
- Include constraints inline with randomize() with {}

USER:
Coverage gap: {gap_yaml}
Base sequence class: {base_class}
Protocol: {protocol}
DUT config: {dut_config}
```

**Output — Generated Sequence:**
```systemverilog
class axi_wrap_255_seq extends axi_base_seq;
  `uvm_object_utils(axi_wrap_255_seq)

  // Coverage target: axi_write_cg.cx_burst_len — WRAP x len_256
  task body();
    axi_seq_item req;
    req = axi_seq_item::type_id::create("req");
    start_item(req);
    if (!req.randomize() with {
      awburst == 2'b10;     // WRAP
      awlen   == 8'hFF;     // 256 beats
      awsize  == 3'h6;      // 64 bytes per beat
      awaddr  == 32'h0;     // wrap-boundary aligned
    }) `uvm_fatal(get_name(), "Randomization failed — WRAP max burst")
    finish_item(req);
  endtask
endclass
```

---

### Agent 3 — Coverage Analysis

**Purpose:** Continuously monitor verification completeness across all types.

**Scheduled trigger:** After every regression merge, every 24 hours, on-demand.

**Output Dashboard:**
```yaml
coverage_snapshot:
  timestamp: <ISO-8601>
  run_id: regression_ww29_nightly

  summary:
    functional_pct:  87.3
    code_stmt_pct:   91.2
    code_branch_pct: 84.7
    toggle_pct:      76.8
    assertion_pct:   93.1

  trend:
    functional_delta_7d: +4.2
    velocity_to_target:  3.1 weeks at current rate

  top_holes:
    - covergroup: axi_write_cg
      coverpoint: cp_awlen
      bin: len_256
      hits: 0
      priority: HIGH
      recommended_agent: test_gen
```

---

### Agent 4 — Coverage Closure

**Purpose:** Translate coverage holes into actionable tests and constraint recommendations.

**LLM Prompt Pattern:**
```
SYSTEM:
You are a DV coverage closure expert. For the coverage hole below,
determine: (1) is it reachable? (2) what stimulus closes it?
(3) provide either a directed UVM sequence OR a constraint addition.
Return structured YAML with your recommendation and confidence level.

USER:
Coverage hole: {hole_description}
Existing constraints: {constraint_block}
Protocol spec reference: {spec_section}
Existing sequences: {sequence_list}
```

---

### Agent 5 — Simulation Control

**Purpose:** Orchestrate the regression farm end-to-end.

**Job Dispatch Schema:**
```yaml
regression_job:
  name: axi_write_closure_ww29
  trigger: coverage_gap_identified
  tests:
    - test_class: axi_wrap_255_seq_test
      seeds: [1, 2, 3, 4, 5, 42, 137, 999]
      plusargs: ["+UVM_VERBOSITY=UVM_MEDIUM"]
      timeout_min: 30
  farm:
    backend: LSF                    # LSF | Slurm | Jenkins | local
    queue: dv_normal
    parallel_jobs: 50
    retry_on_timeout: true
    max_retries: 2
  post_run:
    coverage_merge: true
    report_to: coverage_analysis_agent
    notify_on_fail: true
```

---

### Agent 6 — Regression Analysis

**Purpose:** Cluster and fingerprint failures across large regression runs.

**Clustering Algorithm:**
```python
def cluster_failures(log_files):
    # 1. Extract UVM_ERROR/FATAL messages from all logs
    errors = [extract_error_signature(log) for log in log_files]

    # 2. Normalize: strip timestamps, addresses, seed-specific values
    normalized = [normalize_error(e) for e in errors]

    # 3. Semantic similarity clustering (LLM embeddings or TF-IDF)
    clusters = semantic_cluster(normalized, min_cluster_size=5)

    # 4. Match against historical bug database
    for cluster in clusters:
        cluster.historical_match = bug_db.find_similar(cluster.signature)

    return clusters
```

**Output:**
```
Regression: axi_write_closure_ww29
Total : 400 tests
PASS  : 385 (96.3%)
FAIL  :  15

Cluster 1 — BVALID_Timeout         : 10 failures (66.7%)
  Example seed: 42
  Error: "Slave timeout waiting for BVALID — outstanding=1"
  Historical match: BUG-047 (FIXED ww22) — regression guard SVA missing?
  Recommendation: Check p_bvalid_response SVA disabled in this run

Cluster 2 — WRAP_Addr_Mismatch     : 5 failures (33.3%)
  Example seed: 137
  Error: "Scoreboard: WRAP address mismatch at beat 3"
  Historical match: None — NEW failure
  Recommendation: Escalate to Agent 7 (Debug Intelligence)
```

---

### Agent 7 — Debug Intelligence

**Purpose:** Parse UVM logs and rank likely root causes.

**LLM Prompt Pattern:**
```
SYSTEM:
You are a UVM debug expert. Analyze the log excerpt below and:
1. Classify failure: TB / DUT / Infrastructure / Flaky
2. Rank top 5 root causes by probability
3. Provide exact grep commands to gather more evidence
4. Suggest waveform signals and time window to inspect
5. Check against known TB bug inventory before blaming DUT

USER:
UVM log excerpt (±50 lines around error): {log_excerpt}
Test: {test_name}, Seed: {seed}
Protocol: {protocol}
Recent RTL changes: {cl_list}
Known TB bug inventory: {tb_bug_list}
```

**Output:**
```yaml
debug_analysis:
  classification: DUT         # TB | DUT | Infra | Flaky
  confidence: 0.78

  root_causes:
    - rank: 1
      hypothesis: "WRAP address wrap logic incorrect at max burst length"
      probability: 0.65
      evidence_needed: "AWADDR[5:0] at beat 3 vs expected wrap point"
      grep: "grep -A5 -B5 'WRAP_Addr_Mismatch' sim.log"

    - rank: 2
      hypothesis: "Scoreboard WRAP address prediction formula error"
      probability: 0.25
      evidence_needed: "Check scoreboard predict_wrap_addr() function"

  waveform_hints:
    signals: [AWADDR, AWLEN, AWBURST, AWVALID, AWREADY]
    time_window: "around first mismatch error timestamp"
    verdi_tcl: "wave zoom -from {error_time - 100ns} -to {error_time + 200ns}"

  tb_bug_check:
    checked: true
    match: none                 # No known TB bug matches this pattern
```

---

### Agent 8 — Waveform Analysis

**Purpose:** Autonomous signal tracing over FSDB/VPD/SHM.

**Pattern Detection Example:**
```
AWVALID asserted    @100ns
    ↓
AWREADY accepted    @110ns
    ↓
WLAST observed      @200ns
    ↓
BVALID never        @600ns  ← ANOMALY: timeout threshold exceeded
Root Cause: Outstanding counter stuck at 1
```

**Verdi TCL Auto-generated:**
```tcl
proc add_axi_write_signals {path} {
  foreach sig {AWVALID AWREADY AWADDR AWLEN AWBURST AWSIZE AWID
               WVALID WREADY WDATA WSTRB WLAST
               BVALID BREADY BRESP BID} {
    add wave -noupdate $path/$sig
  }
}
add_axi_write_signals /tb_top/dut/axi_if
wave zoom -from 95ns -to 620ns
```

---

### Agents 9–11 Summary

| Agent | Purpose | Key Output |
|---|---|---|
| 9 — Scoreboard Intelligence | Validate per-transaction correctness in NxM NoC | Match/mismatch report per master→slave path |
| 10 — NoC Traffic Optimization | Close connectivity coverage holes | Directed traffic: missing master→slave paths |
| 11 — DV Milestone | Track project maturity vs. signoff gates | Dashboard: coverage%, bugs open, milestone% |

---

## 18.4 Technology Stack

### LLM Layer
```
Claude (Anthropic)     — code generation, debug analysis, plan extraction
GPT-4o (OpenAI)       — general reasoning, document parsing
Gemini (Google)       — multi-modal, spec parsing with diagrams
Code Llama (Meta)     — local deployment for IP-sensitive environments
```

### RAG Knowledge Base
```
Specifications        → Chunked, embedded, indexed
Vplans                → Structured YAML, semantic indexed
Coverage Reports      → URG parsed, hole catalog
Regression Logs       → Error-normalized, clustered
Bug Database          → Jira/GitHub issues, resolution history
UVM Library           → Code patterns, anti-patterns
Protocol Specs        → AMBA ARM IHI, USB IF, PCI-SIG
```

### Vector Database
```
FAISS     — local, fast, CPU-based
ChromaDB  — persistent, Python-native
Pinecone  — cloud, production-scale
Milvus    — distributed, high-throughput
```

---

## 18.5 MVP Rollout Plan

Deploy in priority order — each stage delivers measurable ROI:

| Phase | Agents | Timeline | ROI |
|---|---|---|---|
| Phase 1 | Planner + Test-Gen | Month 1–2 | Automated vplan, first sequences |
| Phase 2 | Regression Analysis + Coverage Analysis | Month 2–3 | Cluster failures, track holes |
| Phase 3 | Debug Intelligence + Coverage Closure | Month 3–4 | Automated RCA, hole closure |
| Phase 4 | Simulation Control + Dashboard | Month 4–5 | Full automation loop |
| Phase 5 | Waveform + Scoreboard + NoC + Milestone | Month 5–6 | Full ecosystem |

**Total productivity gain at Phase 3: 70–80% of achievable** (per Agentic AI DV Architecture v1.0)

---

## 18.6 Agent Integration Contracts

All agents communicate via structured YAML or JSON. No free-text pipelines between agents.

Each agent exposes:
```yaml
agent_contract:
  input_schema:  <yaml_schema>
  output_schema: <yaml_schema>
  tool_calls:    [<eda_tool_integrations>]
  error_contract:
    on_empty_input:  "Return empty schema with status=NO_INPUT"
    on_tool_failure: "Return status=TOOL_FAILURE with error details"
    on_timeout:      "Return status=TIMEOUT with partial results"
  audit_log:
    enabled: true
    fields: [timestamp, agent_id, input_hash, output_hash, status]
```

**Audit logging is mandatory.** Every agent action must be traceable for DV evidence.
