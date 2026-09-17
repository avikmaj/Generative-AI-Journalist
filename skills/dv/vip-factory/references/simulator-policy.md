# SIMULATOR POLICY
## AVIK VIP Factory · Environment · Portability · Verilator Setup

---

## Primary Free Simulator Stack

```
Ubuntu 22.04 / WSL2
        │
        ├── Verilator 5.050       (primary simulator)
        ├── UVM (Verilator-compatible)
        ├── Z3                    (constraint solver for CRV)
        ├── Python 3.10+          (dv_runner, result parser, regression mgr)
        ├── Make                  (build system)
        ├── GTKWave               (waveform viewer — FST/VCD)
        └── Git                   (version control)
```

### Install commands (Ubuntu/WSL2):

```bash
# Verilator
sudo apt-get install -y verilator

# GTKWave
sudo apt-get install -y gtkwave

# Z3
sudo apt-get install -y z3 python3-z3

# Python tools
pip3 install pyyaml jinja2 pytest

# Verify
verilator --version
gtkwave --version
z3 --version
```

---

## Verilator Simulation Command Pattern

```bash
# Compile + elaborate
verilator --sv --binary \
  -DUVM_NO_DPI \
  --coverage \
  --trace-fst \
  -j 4 \
  -f filelist.f \
  -top tb_top \
  -o simv \
  --Mdir obj_dir

# Run simulation
./obj_dir/simv \
  +UVM_TESTNAME=<test> \
  +UVM_VERBOSITY=UVM_MEDIUM \
  +ntb_random_seed=<seed> \
  +DUMP_WAVES=1 \
  2>&1 | tee transcript.log

# Coverage report
verilator_coverage --annotate obj_dir/coverage.dat \
  --write obj_dir/coverage_merged.dat
```

---

## Waveform Policy

```
Format preference:  FST (smaller, faster)
Fallback:           VCD

When to dump waveforms:
  ALWAYS: on FAIL or NOT_VERIFIED
  OPTIONAL: on PASS (configurable — off by default for speed)

Waveform storage:
  results/<test>/seed_<N>/waveform.fst
  Never delete waveforms for failures.

GTKWave open command:
  gtkwave results/<test>/seed_<N>/waveform.fst &
```

---

## Simulator Portability Policy

```
Verified on Verilator  ≠  Cross-simulator verified

Every signoff document MUST explicitly state per-simulator status:

VERILATOR:  PASS | FAIL | NOT_RUN
VCS:        PASS | FAIL | NOT_RUN
QUESTA:     PASS | FAIL | NOT_RUN
XCELIUM:    PASS | FAIL | NOT_RUN

NOT_RUN IS NOT PASS.
NOT_RUN must never be reported as PASS, implied to be PASS,
or omitted from the signoff document.
```

### Portability notes — Verilator vs event-driven simulators:

| Feature | Verilator 5.050 | VCS/Questa/Xcelium |
|---|---|---|
| UVM support | Active development — use UVM-compatible subset | Full UVM 1.2/1.1 |
| CRV | Via Z3 solver | Built-in SV randomize() |
| FSM coverage | Supported | Full |
| Covergroups | Supported in 5.x | Full |
| X propagation | 2-state by default | 4-state (X/Z) |
| DPI-C | Supported | Full |
| Timing | Cycle-accurate | Full timing |

**Always note Verilator limitations** in signoff. Code written for Verilator may need
adaptation for 4-state simulation, DPI, or timing-sensitive constructs.

---

## CI — GitHub Actions

```yaml
# .github/workflows/dv_regression.yml
name: DV Regression

on:
  push:
    branches: ['feature/**', 'hotfix/**']
  pull_request:
    branches: ['develop', 'main']

jobs:
  L0_compile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Verilator
        run: sudo apt-get install -y verilator
      - name: Compile
        run: make compile VIP=<vip>

  L1_smoke:
    needs: L0_compile
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Smoke regression
        run: python3 dv_runner/regression.py --tier L1 --vip <vip>
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: smoke-results
          path: results/
```
