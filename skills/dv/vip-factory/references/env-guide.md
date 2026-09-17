# AVIK VIP FACTORY — Environment Guide
## Item 9: Verilator + UVM + Z3 + GTKWave

---

## Quick Install (Ubuntu 22.04 / WSL2)

```bash
chmod +x env/setup_env.sh
./env/setup_env.sh
source ~/.bashrc
python3 dv_runner/dv_runner.py env   # verify all tools found
```

---

## Manual Install — Step by Step

### Verilator 5.x
```bash
sudo apt-get install -y verilator
verilator --version   # must show 5.x
```

If apt gives Verilator 4.x (older Ubuntu):
```bash
# Build from source
sudo apt-get install -y git autoconf flex bison help2man perl
git clone https://github.com/verilator/verilator
cd verilator
autoconf
./configure
make -j$(nproc)
sudo make install
```

### GTKWave
```bash
sudo apt-get install -y gtkwave
gtkwave --version
# Open waveform: gtkwave results/<test>/seed_N/waveform.fst &
```

### Z3 (constraint solver)
```bash
sudo apt-get install -y z3 python3-z3
z3 --version
```

### Python 3 + packages
```bash
sudo apt-get install -y python3 python3-pip
pip3 install pyyaml jinja2 pytest colorama tabulate
```

### Git + GitHub CLI
```bash
sudo apt-get install -y git
# GitHub CLI (for CI integration)
(type -p curl >/dev/null || sudo apt install curl -y) \
&& curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
   | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) \
   signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
   https://cli.github.com/packages stable main" \
   | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
gh auth login
```

---

## Environment Variables

Add to `~/.bashrc`:
```bash
export UVM_HOME=$HOME/uvm/src           # UVM source directory
export VIP_FACTORY_ROOT=/path/to/factory
export VERILATOR_ROOT=/usr/share/verilator
```

---

## Verilator + UVM Compile Command Reference

```bash
verilator --sv --binary \
  -DUVM_NO_DPI \
  +incdir+$UVM_HOME/src \
  $UVM_HOME/src/uvm_pkg.sv \
  --coverage \
  --trace-fst \
  -j $(nproc) \
  -f vip/<vip>/tb/filelist.f \
  -top tb_top \
  -o obj_dir/<vip>/simv \
  --Mdir obj_dir/<vip>
```

## Run Command Reference

```bash
# Single test
./obj_dir/<vip>/simv \
  +UVM_TESTNAME=<test> \
  +UVM_VERBOSITY=UVM_MEDIUM \
  +ntb_random_seed=<seed>

# With waveform
./obj_dir/<vip>/simv \
  +UVM_TESTNAME=<test> \
  +ntb_random_seed=<seed> \
  +DUMP_WAVES=1

# Open waveform
gtkwave results/<test>/seed_<N>/waveform.fst &
```

---

## Tool Verification Checklist

After setup, run and confirm all PASS:
```bash
python3 dv_runner/dv_runner.py env
```

Expected output:
```
[ENV] Verilator: Verilator 5.050 ...
✓ verilator found
✓ gtkwave found
✓ z3 found
✓ python3 found
✓ git found
✓ make found
```

Any ✗ = that tool needs to be installed before simulation will work.

---

## Waveform Workflow

```
Simulation (FAIL)
      ↓
waveform.fst generated in results/<test>/seed_<N>/
      ↓
gtkwave results/<test>/seed_<N>/waveform.fst &
      ↓
Add signals: Edit → Insert → signal names
      ↓
Zoom to error timestamp from transcript.log
      ↓
Root cause analysis
```

**Always preserve waveform.fst for every FAIL — never delete.**
