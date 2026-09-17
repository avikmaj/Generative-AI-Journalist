# TB INFRASTRUCTURE GUIDE
## AVIK VIP Factory · Makefile · compile.sh · run.sh · regression.sh

---

## File Inventory

| File | Purpose | When to use |
|---|---|---|
| `Makefile` | Primary build system | Daily use — `make` commands |
| `compile.sh` | Standalone compile | CI / direct shell / debugging |
| `run.sh` | Single test execution | Debug / targeted run |
| `regression.sh` | Regression tiers L0–L5 | Regression campaigns |
| `dv_runner.py` | Python execution interface | Programmatic / CI integration |

All tools are equivalent paths to the same simulation. Use whichever fits
the context — they all produce identical `result.json` artifacts.

---

## Quick Reference

### Compile
```bash
make compile VIP=axi4
# or
./compile.sh axi4
# or
python3 dv_runner/dv_runner.py compile --vip axi4
```

### Run single test
```bash
make run VIP=axi4 TEST=axi4_smoke_test SEED=1
make run VIP=axi4 TEST=axi4_smoke_test SEED=1 WAVES=1   # with waveform
# or
./run.sh axi4 axi4_smoke_test 1
./run.sh axi4 axi4_smoke_test 1 1 UVM_HIGH              # waves + high verbosity
```

### Regression tiers
```bash
make regress-l0 VIP=axi4    # L0: compile only (GATE 2)
make regress-l1 VIP=axi4    # L1: smoke (GATE 3)
make regress-l2 VIP=axi4    # L2: directed (GATE 4)
make regress-l3 VIP=axi4    # L3: random 100 seeds (GATE 5)
make regress-l4 VIP=axi4    # L4: stress 1000 seeds
make regress-l5 VIP=axi4    # L5: full signoff (GATE 9)
# or
./regression.sh axi4 L1
./regression.sh axi4 L3 100
```

### Open waveform
```bash
make waves VIP=axi4 TEST=axi4_smoke_test SEED=1
# or
gtkwave results/axi4/axi4_smoke_test/seed_1/waveform.fst &
```

### Coverage report
```bash
make coverage VIP=axi4
```

### Environment check
```bash
make env
```

### Clean
```bash
make clean VIP=axi4      # clean one VIP
make clean-all           # clean all (preserves results/ and regression_db/)
```

---

## Result Artifact — result.json

Every test run produces:
```
results/<vip>/<test>/seed_<N>/
├── result.json       ← machine-readable verdict (STATUS field is truth)
├── transcript.log    ← full simulator output
└── waveform.fst      ← only when WAVES=1 or on FAIL
```

STATUS values: `PASS | FAIL | NOT_VERIFIED | EXPECTED_FAILURE_DETECTED | UNEXPECTED_PASS`

**PASS requires ALL:**
- exit_code = 0
- uvm_errors = 0
- uvm_fatals = 0
- assertion_failures = 0
- scoreboard_errors = 0
- UVM report summary present in log

**NOT_VERIFIED** = UVM report summary not found — treat as FAIL, never as PASS.

---

## Regression Database

Every regression run writes:
```
regression_db/runs/<YYYYMMDD_HHMMSS>_<vip>_<tier>/
├── summary.json        ← total/pass/fail/not_verified/pass_pct/status
├── compile.log
└── <test>_seed_<N>.log ← per-test run log
```

Never delete regression_db/ — it is the historical evidence archive.

---

## Waveform Policy

```
ALWAYS dump waveform when: FAIL or NOT_VERIFIED
OPTIONAL when:             PASS (off by default for speed)

Enable: make run WAVES=1  or  ./run.sh <vip> <test> <seed> 1
Format: FST (smaller than VCD — preferred)
View:   gtkwave <waveform.fst> &
        make waves VIP=<vip> TEST=<test> SEED=<N>
```

Waveforms for FAILed tests must never be deleted.

---

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `UVM_HOME` | `$HOME/uvm/src` | UVM source directory |
| `VIP` | `axi4` | VIP name (make target) |
| `TEST` | `<vip>_smoke_test` | Test class name |
| `SEED` | `1` | Random seed |
| `TIER` | `L1` | Regression tier |
| `WAVES` | `0` | Enable waveform dump |
| `VERBOSITY` | `UVM_MEDIUM` | UVM verbosity level |
| `JOBS` | `nproc` | Parallel compile jobs |

---

## Gate to Make Target Mapping

| Gate | Description | Make target |
|---|---|---|
| GATE 2 | Compile PASS | `make regress-l0 VIP=<vip>` |
| GATE 3 | Smoke PASS | `make regress-l1 VIP=<vip>` |
| GATE 4 | Directed PASS | `make regress-l2 VIP=<vip>` |
| GATE 5 | Random PASS | `make regress-l3 VIP=<vip>` |
| GATE 9 | Full regression | `make regress-l5 VIP=<vip>` |

---

## Adding a New VIP to the Build System

No changes to Makefile, compile.sh, run.sh, or regression.sh needed.
They are VIP-agnostic — driven entirely by `VIP=<name>` parameter.

Only requirement: `vip/<name>/tb/filelist.f` must exist and be correct.

```bash
# New VIP immediately works:
make env
make compile VIP=apb4
make regress-l1 VIP=apb4
```
