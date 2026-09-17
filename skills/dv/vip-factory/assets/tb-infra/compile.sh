#!/bin/bash
# ==============================================================================
# AVIK VIP FACTORY — compile.sh
# Standalone VIP testbench compile script
# Usage: ./compile.sh <vip> [extra_flags]
# Example: ./compile.sh axi4
#          ./compile.sh apb4 +define+APB4_PSTRB_ENABLE
# ==============================================================================

set -e

# ── Colours ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
pass()  { echo -e "${GREEN}[PASS]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }
info()  { echo -e "${YELLOW}[INFO]${NC}  $1"; }
step()  { echo -e "\n${GREEN}──────────────────────────────────────────${NC}"; \
          echo -e "${GREEN}  $1${NC}"; \
          echo -e "${GREEN}──────────────────────────────────────────${NC}"; }

# ── Arguments ──────────────────────────────────────────────────────────────────
VIP=${1:?"Usage: $0 <vip> [extra_flags]  e.g. $0 axi4"}
shift
EXTRA_FLAGS="$@"

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIP_DIR="${SCRIPT_DIR}/vip/${VIP}"
TB_DIR="${VIP_DIR}/tb"
FILELIST="${TB_DIR}/filelist.f"
OBJ_DIR="${SCRIPT_DIR}/obj_dir/${VIP}"
SIMV="${OBJ_DIR}/simv"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/${VIP}_compile.log"
UVM_HOME="${UVM_HOME:-${HOME}/uvm/src}"

# ── Banner ─────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         AVIK VIP FACTORY — Compile                  ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  VIP      : ${VIP}"
echo "║  Filelist : ${FILELIST}"
echo "║  Output   : ${SIMV}"
echo "║  UVM_HOME : ${UVM_HOME}"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── Pre-flight checks ──────────────────────────────────────────────────────────
step "Step 1 — Pre-flight checks"

command -v verilator &>/dev/null || fail "verilator not found — run: sudo apt-get install verilator"
info "Verilator: $(verilator --version | head -1)"

[ -f "${FILELIST}" ] || fail "Filelist not found: ${FILELIST}"
info "Filelist: ${FILELIST}"

[ -f "${UVM_HOME}/uvm_pkg.sv" ] || \
  fail "UVM not found at ${UVM_HOME} — set UVM_HOME env var"
info "UVM: ${UVM_HOME}/uvm_pkg.sv"

# ── Create directories ─────────────────────────────────────────────────────────
mkdir -p "${OBJ_DIR}" "${LOG_DIR}"

# ── Compile ────────────────────────────────────────────────────────────────────
step "Step 2 — Compile VIP=${VIP}"

COMPILE_CMD=(
  verilator
  --sv
  --binary
  -DUVM_NO_DPI
  +incdir+"${UVM_HOME}"/src
  --coverage
  --trace-fst
  -j "$(nproc)"
  --Mdir "${OBJ_DIR}"
  -o "${SIMV}"
  -f "${FILELIST}"
  -top tb_top
  ${EXTRA_FLAGS}
)

info "Command: ${COMPILE_CMD[*]}"
echo ""

# Run compile — capture output and tee to log
set +e
"${COMPILE_CMD[@]}" 2>&1 | tee "${LOG_FILE}"
COMPILE_EXIT=${PIPESTATUS[0]}
set -e

# ── Result ─────────────────────────────────────────────────────────────────────
step "Step 3 — Result"

if [ ${COMPILE_EXIT} -ne 0 ]; then
  fail "Compile FAILED (exit=${COMPILE_EXIT}) — see ${LOG_FILE}"
fi

# Verify simv was created
[ -f "${SIMV}" ] || fail "simv not created despite exit=0 — check log: ${LOG_FILE}"

# Check for warnings treated as errors
WARN_COUNT=$(grep -c "Warning" "${LOG_FILE}" 2>/dev/null || echo 0)
ERROR_COUNT=$(grep -c "Error\|error:" "${LOG_FILE}" 2>/dev/null || echo 0)

info "Warnings  : ${WARN_COUNT}"
info "Errors    : ${ERROR_COUNT}"
info "Output    : ${SIMV} ($(du -h ${SIMV} | cut -f1))"
info "Log       : ${LOG_FILE}"

echo ""
pass "Compile: PASS — VIP=${VIP}"
echo ""
echo "  Run test:       ./run.sh ${VIP} ${VIP}_smoke_test 1"
echo "  Make target:    make run VIP=${VIP} TEST=${VIP}_smoke_test SEED=1"
echo "  dv_runner:      python3 dv_runner/dv_runner.py run --vip ${VIP} --test ${VIP}_smoke_test --seed 1"
echo ""
echo "STATUS: PASS"
echo "NEXT:   Run L1 smoke regression to advance to GATE 3"
