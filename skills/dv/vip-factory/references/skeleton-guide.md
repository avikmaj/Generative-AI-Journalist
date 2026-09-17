# VIP SKELETON — Usage Guide
## AVIK VIP Factory · Items 11 + 12: Reusable VIP Skeleton + Test/Sequence Templates

---

## What the Skeleton Provides

```
skeleton/
├── uvm/
│   ├── transaction/vip_seq_item.sv     → <vip>_seq_item class
│   ├── agent/vip_agent.sv              → driver + monitor + agent + agent_cfg
│   ├── env/vip_env.sv                  → env + env_cfg + scoreboard + coverage + assertions
│   └── pkg/vip_pkg.sv                  → UVM package (includes all above)
├── tb/
│   └── vip_tb_top.sv                   → tb_top + <vip>_if interface + filelist.f
├── tests/
│   └── vip_tests.sv                    → base, smoke, write, read, random,
│                                          error, stress, backpressure, reset
└── sequences/
    └── vip_sequences.sv                → base, write, read, random,
                                          error, backpressure sequences
```

---

## How to Create a New VIP (e.g. APB4)

### Step 1 — Copy the skeleton

```bash
cp -r factory/skeleton vip/apb4
```

### Step 2 — Global search and replace

```bash
cd vip/apb4
# Replace <vip> with apb4 (lowercase)
find . -type f | xargs sed -i 's/<vip>/apb4/g'
# Replace <VIP> with APB4 (uppercase — for comments)
find . -type f | xargs sed -i 's/<VIP>/APB4/g'
# Replace <dut_module> with your actual DUT module name
find . -type f | xargs sed -i 's/<dut_module>/apb4_slave/g'
```

### Step 3 — Rename files

```bash
find . -name "vip_*" | while read f; do
  mv "$f" "${f/vip_/apb4_}"
done
find . -name "*vip*" | while read f; do
  mv "$f" "${f/vip/apb4}"
done
```

### Step 4 — Implement the protocol-specific TODOs

Open each file and fill in the TODO sections:

| File | TODO |
|---|---|
| `uvm/transaction/apb4_seq_item.sv` | Add APB4 fields: PADDR, PWDATA, PRDATA, PWRITE, PSTRB, PPROT |
| `tb/apb4_if.sv` | Add APB4 signals: PSEL, PENABLE, PREADY, PSLVERR |
| `uvm/agent/apb4_driver.sv` | Implement APB4 SETUP + ACCESS phase driving |
| `uvm/agent/apb4_monitor.sv` | Implement APB4 bus observation (sample at PENABLE+PREADY) |
| `uvm/env/apb4_env.sv` | Implement APB4 predictor (read after write) |
| `uvm/assertions/apb4_assertions.sv` | Add APB4 SVA: p_psel_before_penable, p_pready_response |
| `uvm/coverage/apb4_coverage.sv` | Add APB4 coverpoints: PADDR regions, PSTRB, PSLVERR, wait states |

### Step 5 — Compile (L0)

```bash
python3 dv_runner/dv_runner.py compile --vip apb4
```

### Step 6 — Run smoke test (L1)

```bash
python3 dv_runner/dv_runner.py run --vip apb4 --test apb4_smoke_test --seed 1
# Expected: STATUS = PASS
```

### Step 7 — Run L1 regression

```bash
python3 dv_runner/dv_runner.py regress --vip apb4 --tier L1
```

---

## Skeleton Coverage — What Each File Covers

| File | Layer | What it implements |
|---|---|---|
| `vip_seq_item.sv` | Transaction | Fields, constraints, convert2string, do_compare |
| `vip_agent.sv` | Agent | Driver, monitor, agent, agent_cfg — all in one file |
| `vip_env.sv` | Environment | Env, env_cfg, scoreboard, coverage, assertions |
| `vip_pkg.sv` | Package | Includes all above in dependency order |
| `vip_tb_top.sv` | Testbench | tb_top, interface, filelist.f |
| `vip_tests.sv` | Tests | base, smoke, write, read, random, error, stress, backpressure, reset |
| `vip_sequences.sv` | Sequences | base, write, read, random, error, backpressure |

---

## VIP Checklist — Before First L1 Run

☐ All `<vip>` placeholders replaced with actual protocol name
☐ Interface signals match DUT port list
☐ Driver implements correct protocol phase timing
☐ Monitor samples at correct handshake point
☐ Scoreboard predict() implements correct expected response
☐ Coverage coverpoints match vplan coverage model
☐ SVA assertions added for all protocol invariants
☐ Each assert has a corresponding cover (vacuity check)
☐ filelist.f includes all files in correct order
☐ tb_top binds DUT ports to interface signals
☐ Compile passes clean (L0: PASS)
