#!/bin/bash
# ==============================================================================
# AVIK VIP FACTORY — run.sh
# Standalone single test simulation script
# Usage: ./run.sh <vip> <test> <seed> [waves=0|1] [verbosity]
# Example: ./run.sh axi4 axi4_smoke_test 1
#          ./run.sh axi4 axi4_random_test 42 1 UVM_HIGH
# ==============================================================================

set -e

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
pass()  { echo -e "${GREEN}[PASS]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; }
info()  { echo -e "${YELLOW}[INFO]${NC}  $1"; }
step()  { echo -e "\n${GREEN}── $1 ${NC}"; }

# ── Arguments ──────────────────────────────────────────────────────────────────
VIP=${1:?"Usage: $0 <vip> <test> <seed> [waves=0|1] [verbosity]"}
TEST=${2:?"Usage: $0 <vip> <test> <seed>"}
SEED=${3:?"Usage: $0 <vip> <test> <seed>"}
WAVES=${4:-0}
VERBOSITY=${5:-UVM_MEDIUM}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIMV="${SCRIPT_DIR}/obj_dir/${VIP}/simv"
RESULT_DIR="${SCRIPT_DIR}/results/${VIP}/${TEST}/seed_${SEED}"
LOG_FILE="${RESULT_DIR}/transcript.log"
WAVE_FILE="${RESULT_DIR}/waveform.fst"
RESULT_JSON="${RESULT_DIR}/result.json"

# ── Banner ─────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         AVIK VIP FACTORY — Run Test                 ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  VIP        : ${VIP}"
echo "║  TEST       : ${TEST}"
echo "║  SEED       : ${SEED}"
echo "║  WAVES      : ${WAVES}"
echo "║  VERBOSITY  : ${VERBOSITY}"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── Pre-flight ─────────────────────────────────────────────────────────────────
step "Pre-flight"
[ -f "${SIMV}" ] || {
  fail "simv not found: ${SIMV}"
  echo "  Run compile first: ./compile.sh ${VIP}"
  echo "  Or:                make compile VIP=${VIP}"
  exit 1
}
info "simv: ${SIMV}"
mkdir -p "${RESULT_DIR}"

# ── Build plusargs ─────────────────────────────────────────────────────────────
PLUSARGS=(
  +UVM_TESTNAME="${TEST}"
  +UVM_VERBOSITY="${VERBOSITY}"
  +ntb_random_seed="${SEED}"
)
[ "${WAVES}" = "1" ] && PLUSARGS+=(+DUMP_WAVES=1 +WAVE_FILE="${WAVE_FILE}")

# ── Run simulation ─────────────────────────────────────────────────────────────
step "Running simulation"
info "Command: ${SIMV} ${PLUSARGS[*]}"
echo ""

START_TIME=$(date +%s)
set +e
"${SIMV}" "${PLUSARGS[@]}" 2>&1 | tee "${LOG_FILE}"
SIM_EXIT=${PIPESTATUS[0]}
set -e
END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))

# ── Parse result ───────────────────────────────────────────────────────────────
step "Parsing result"

# Extract UVM counts from log
UVM_ERRORS=$(grep -oP 'UVM_ERROR\s*:\s*\K\d+' "${LOG_FILE}" | tail -1 || echo "-1")
UVM_FATALS=$(grep -oP 'UVM_FATAL\s*:\s*\K\d+' "${LOG_FILE}" | tail -1 || echo "-1")
ASSERT_FAILS=$(grep -c "Assertion failed\|ASSERTION_FAIL" "${LOG_FILE}" 2>/dev/null || echo "0")
SB_ERRORS=$(grep -c "SCOREBOARD ERROR\|MISMATCH" "${LOG_FILE}" 2>/dev/null || echo "0")

info "Exit code       : ${SIM_EXIT}"
info "UVM_ERROR count : ${UVM_ERRORS}"
info "UVM_FATAL count : ${UVM_FATALS}"
info "Assertion fails : ${ASSERT_FAILS}"
info "Scoreboard errs : ${SB_ERRORS}"
info "Runtime         : ${RUNTIME}s"

# ── Determine status ───────────────────────────────────────────────────────────
# PASS only when ALL conditions met — never inferred
if [ "${SIM_EXIT}" -eq 0 ] && \
   [ "${UVM_ERRORS}" = "0" ] && \
   [ "${UVM_FATALS}" = "0" ] && \
   [ "${ASSERT_FAILS}" = "0" ] && \
   [ "${SB_ERRORS}" = "0" ] && \
   grep -q "UVM_ERROR :    0" "${LOG_FILE}" 2>/dev/null && \
   grep -q "UVM_FATAL :    0" "${LOG_FILE}" 2>/dev/null; then
  STATUS="PASS"
elif [ "${UVM_ERRORS}" = "-1" ] || [ "${UVM_FATALS}" = "-1" ]; then
  STATUS="NOT_VERIFIED"   # UVM report summary not found — cannot confirm PASS
else
  STATUS="FAIL"
fi

# ── Write result.json ──────────────────────────────────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "UNKNOWN")
VERILATOR_VER=$(verilator --version 2>/dev/null | head -1 || echo "UNKNOWN")

cat > "${RESULT_JSON}" << EOF
{
  "test":               "${TEST}",
  "seed":               ${SEED},
  "simulator":          "verilator",
  "simulator_version":  "${VERILATOR_VER}",
  "commit_sha":         "${COMMIT}",
  "timestamp":          "${TIMESTAMP}",
  "status":             "${STATUS}",
  "exit_code":          ${SIM_EXIT},
  "uvm_errors":         ${UVM_ERRORS},
  "uvm_fatals":         ${UVM_FATALS},
  "assertion_failures": ${ASSERT_FAILS},
  "scoreboard_errors":  ${SB_ERRORS},
  "runtime_seconds":    ${RUNTIME},
  "waveform":           "${WAVES}" == "1" ? "${WAVE_FILE}" : "",
  "log":                "${LOG_FILE}"
}
EOF

# ── Final result ───────────────────────────────────────────────────────────────
step "Result"
info "Result JSON : ${RESULT_JSON}"
info "Log         : ${LOG_FILE}"
[ "${WAVES}" = "1" ] && [ -f "${WAVE_FILE}" ] && \
  info "Waveform    : ${WAVE_FILE} — open with: gtkwave ${WAVE_FILE} &"

echo ""
if [ "${STATUS}" = "PASS" ]; then
  pass "STATUS: PASS — ${TEST} seed=${SEED}"
elif [ "${STATUS}" = "NOT_VERIFIED" ]; then
  echo -e "${YELLOW}[NOT_VERIFIED]${NC} UVM report summary not found in log"
  echo "  UVM_ERROR/FATAL counts could not be confirmed"
  echo "  NOT_VERIFIED is NOT PASS — investigate log: ${LOG_FILE}"
else
  fail "STATUS: FAIL — ${TEST} seed=${SEED}"
  echo "  Investigate: ${LOG_FILE}"
  echo "  Waveform:    make run WAVES=1 VIP=${VIP} TEST=${TEST} SEED=${SEED}"
fi
echo ""
