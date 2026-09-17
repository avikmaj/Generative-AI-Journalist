# ==============================================================================
# AVIK VIP FACTORY — Makefile
# TB Infrastructure Build System
# Usage: make help
# ==============================================================================

# ── Default VIP and test ───────────────────────────────────────────────────────
VIP        ?= axi4
TEST       ?= $(VIP)_smoke_test
SEED       ?= 1
TIER       ?= L1
WAVES      ?= 0
VERBOSITY  ?= UVM_MEDIUM
JOBS       ?= $(shell nproc)

# ── Directories ────────────────────────────────────────────────────────────────
VIP_DIR    := vip/$(VIP)
TB_DIR     := $(VIP_DIR)/tb
OBJ_DIR    := obj_dir/$(VIP)
RESULTS    := results/$(VIP)
LOG_DIR    := logs
COV_DIR    := coverage_db/$(VIP)
REGDB_DIR  := regression_db

# ── Tool ───────────────────────────────────────────────────────────────────────
VERILATOR  := verilator
PYTHON     := python3

# ── Filelist ───────────────────────────────────────────────────────────────────
FILELIST   := $(TB_DIR)/filelist.f
SIMV       := $(OBJ_DIR)/simv

# ── UVM ────────────────────────────────────────────────────────────────────────
UVM_HOME   ?= $(HOME)/uvm/src
UVM_SRC    := $(UVM_HOME)/uvm_pkg.sv

# ── Verilator flags ────────────────────────────────────────────────────────────
VFLAGS := \
  --sv \
  --binary \
  -DUVM_NO_DPI \
  +incdir+$(UVM_HOME)/src \
  --coverage \
  --trace-fst \
  -j $(JOBS) \
  --Mdir $(OBJ_DIR) \
  -o $(SIMV)

# ── Simulation plusargs ────────────────────────────────────────────────────────
PLUSARGS := \
  +UVM_TESTNAME=$(TEST) \
  +UVM_VERBOSITY=$(VERBOSITY) \
  +ntb_random_seed=$(SEED)

ifeq ($(WAVES),1)
  PLUSARGS += +DUMP_WAVES=1
endif

# ==============================================================================
# TARGETS
# ==============================================================================

.PHONY: help all compile run regress regress-l0 regress-l1 regress-l2 \
        regress-l3 regress-l4 regress-l5 coverage waves clean clean-all \
        env check lint

# ── Help ───────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════╗"
	@echo "║           AVIK VIP FACTORY — Build System                ║"
	@echo "╠══════════════════════════════════════════════════════════╣"
	@echo "║  make env                    Verify tool installation    ║"
	@echo "║  make compile   VIP=axi4     Compile VIP testbench       ║"
	@echo "║  make run       VIP=axi4     Run single test             ║"
	@echo "║                 TEST=axi4_smoke_test SEED=1 WAVES=1      ║"
	@echo "║  make regress-l0 VIP=axi4   Compile only (L0)           ║"
	@echo "║  make regress-l1 VIP=axi4   Smoke regression (L1)       ║"
	@echo "║  make regress-l2 VIP=axi4   Directed regression (L2)    ║"
	@echo "║  make regress-l3 VIP=axi4   Random regression (L3)      ║"
	@echo "║  make regress-l4 VIP=axi4   Stress regression (L4)      ║"
	@echo "║  make regress-l5 VIP=axi4   Full signoff regression (L5)║"
	@echo "║  make coverage  VIP=axi4    Merge and report coverage    ║"
	@echo "║  make waves     VIP=axi4    Open waveform in GTKWave     ║"
	@echo "║                 TEST=<test> SEED=<N>                     ║"
	@echo "║  make clean     VIP=axi4    Clean VIP build artifacts    ║"
	@echo "║  make clean-all             Clean all VIP artifacts      ║"
	@echo "╚══════════════════════════════════════════════════════════╝"
	@echo ""

# ── Environment check ──────────────────────────────────────────────────────────
env:
	@echo "[ENV] Checking tool installation..."
	@$(PYTHON) dv_runner/dv_runner.py env
	@echo "[ENV] Checking UVM_HOME..."
	@test -f $(UVM_SRC) || (echo "[ERROR] UVM not found at $(UVM_HOME)" && exit 1)
	@echo "[ENV] UVM found: $(UVM_SRC)"
	@echo "[ENV] STATUS: READY"

# ── Compile (L0 gate) ──────────────────────────────────────────────────────────
compile: $(SIMV)

$(SIMV): $(FILELIST)
	@echo "[COMPILE] VIP=$(VIP) ..."
	@mkdir -p $(OBJ_DIR) $(LOG_DIR)
	@$(VERILATOR) $(VFLAGS) \
	  -f $(FILELIST) \
	  -top tb_top \
	  2>&1 | tee $(LOG_DIR)/$(VIP)_compile.log
	@if [ $$? -ne 0 ]; then \
	  echo "[COMPILE] STATUS: FAIL — see $(LOG_DIR)/$(VIP)_compile.log"; \
	  exit 1; \
	fi
	@echo "[COMPILE] STATUS: PASS"

# ── Run single test ────────────────────────────────────────────────────────────
run: compile
	@echo "[RUN] VIP=$(VIP) TEST=$(TEST) SEED=$(SEED) WAVES=$(WAVES)"
	@mkdir -p $(RESULTS)/$(TEST)/seed_$(SEED)
	@$(SIMV) $(PLUSARGS) \
	  2>&1 | tee $(RESULTS)/$(TEST)/seed_$(SEED)/transcript.log
	@$(PYTHON) dv_runner/dv_runner.py parse \
	  --log $(RESULTS)/$(TEST)/seed_$(SEED)/transcript.log \
	  --test $(TEST) \
	  --seed $(SEED) \
	  --vip $(VIP)
	@echo "[RUN] STATUS: see $(RESULTS)/$(TEST)/seed_$(SEED)/result.json"

# ── Regression tiers ───────────────────────────────────────────────────────────
regress-l0: compile
	@echo "[L0] Compile gate: PASS"

regress-l1: compile
	@echo "[L1] Running smoke regression — VIP=$(VIP)"
	@$(PYTHON) dv_runner/dv_runner.py regress \
	  --vip $(VIP) --tier L1
	@echo "[L1] STATUS: see regression_db/"

regress-l2: compile
	@echo "[L2] Running directed regression — VIP=$(VIP)"
	@$(PYTHON) dv_runner/dv_runner.py regress \
	  --vip $(VIP) --tier L2

regress-l3: compile
	@echo "[L3] Running random regression — VIP=$(VIP) (100 seeds)"
	@$(PYTHON) dv_runner/dv_runner.py regress \
	  --vip $(VIP) --tier L3

regress-l4: compile
	@echo "[L4] Running stress regression — VIP=$(VIP) (1000 seeds)"
	@$(PYTHON) dv_runner/dv_runner.py regress \
	  --vip $(VIP) --tier L4

regress-l5: compile
	@echo "[L5] Running full signoff regression — VIP=$(VIP)"
	@$(PYTHON) dv_runner/dv_runner.py regress \
	  --vip $(VIP) --tier L5
	@echo "[L5] STATUS: see regression_db/ — independent review required before GATE 11"

# Alias
regress: regress-l1

# ── Coverage ───────────────────────────────────────────────────────────────────
coverage:
	@echo "[COVERAGE] Merging coverage databases — VIP=$(VIP)"
	@mkdir -p $(COV_DIR)/merged
	@verilator_coverage \
	  --annotate $(COV_DIR)/merged \
	  --write $(COV_DIR)/merged/coverage_merged.dat \
	  $(COV_DIR)/*.dat 2>/dev/null || true
	@echo "[COVERAGE] Report: $(COV_DIR)/merged/"
	@$(PYTHON) dv_runner/dv_runner.py coverage --vip $(VIP)

# ── Waveform ───────────────────────────────────────────────────────────────────
waves:
	@WAVE_FILE=$(RESULTS)/$(TEST)/seed_$(SEED)/waveform.fst; \
	if [ -f $$WAVE_FILE ]; then \
	  echo "[WAVES] Opening $$WAVE_FILE"; \
	  gtkwave $$WAVE_FILE &; \
	else \
	  echo "[WAVES] Not found: $$WAVE_FILE"; \
	  echo "[WAVES] Re-run with: make run WAVES=1 TEST=$(TEST) SEED=$(SEED)"; \
	fi

# ── Clean ──────────────────────────────────────────────────────────────────────
clean:
	@echo "[CLEAN] VIP=$(VIP)"
	@rm -rf $(OBJ_DIR) $(LOG_DIR)/$(VIP)_compile.log
	@echo "[CLEAN] Done"

clean-all:
	@echo "[CLEAN-ALL] Removing all build artifacts"
	@rm -rf obj_dir/ logs/
	@echo "[CLEAN-ALL] Done — results/ and regression_db/ preserved"

# ── Lint (optional — requires verilator lint mode) ────────────────────────────
lint:
	@echo "[LINT] VIP=$(VIP)"
	@$(VERILATOR) --lint-only --sv \
	  +incdir+$(UVM_HOME)/src \
	  -f $(FILELIST) \
	  2>&1 | tee $(LOG_DIR)/$(VIP)_lint.log
	@echo "[LINT] Report: $(LOG_DIR)/$(VIP)_lint.log"
