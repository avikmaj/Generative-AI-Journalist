#!/bin/bash
# ==============================================================================
# AVIK VIP FACTORY — regression.sh
# Standalone regression script — L0 through L5
# Usage: ./regression.sh <vip> <tier> [seed_count]
# Example: ./regression.sh axi4 L1
#          ./regression.sh axi4 L3 100
# ==============================================================================

set -e

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
pass()  { echo -e "${GREEN}[PASS]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; }
info()  { echo -e "${YELLOW}[INFO]${NC}  $1"; }

VIP=${1:?"Usage: $0 <vip> <tier> [seed_count]  e.g. $0 axi4 L1"}
TIER=${2:?"Tier required: L0 L1 L2 L3 L4 L5"}
SEED_COUNT=${3:-10}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_ID="${TIMESTAMP}_${VIP}_${TIER}"
REGDB_DIR="${SCRIPT_DIR}/regression_db/runs/${RUN_ID}"
mkdir -p "${REGDB_DIR}"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       AVIK VIP FACTORY — Regression                 ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  VIP    : ${VIP}"
echo "║  TIER   : ${TIER}"
echo "║  RUN_ID : ${RUN_ID}"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── L0: Compile only ───────────────────────────────────────────────────────────
if [ "${TIER}" = "L0" ]; then
  echo "[L0] Compile gate"
  ./compile.sh "${VIP}"
  echo ""
  echo "STATUS: PASS"
  echo "GATE 2: PASS — compile clean"
  echo "NEXT: Run L1 smoke: ./regression.sh ${VIP} L1"
  exit 0
fi

# ── Compile first (always) ─────────────────────────────────────────────────────
echo "[COMPILE] Building ${VIP}..."
./compile.sh "${VIP}" > "${REGDB_DIR}/compile.log" 2>&1 || {
  fail "Compile FAILED — GATE 2: FAIL"
  cat "${REGDB_DIR}/compile.log"
  exit 1
}
echo "[COMPILE] PASS"

# ── Define test lists per tier ─────────────────────────────────────────────────
case "${TIER}" in
  L1) TESTS=("${VIP}_smoke_test")
      FIXED_SEEDS=(1 2 3) ;;
  L2) TESTS=("${VIP}_write_test" "${VIP}_read_test" "${VIP}_burst_test"
             "${VIP}_backpressure_test" "${VIP}_reset_test" "${VIP}_error_test")
      FIXED_SEEDS=(1 2 3 4 5 6 7 8 9 10) ;;
  L3) TESTS=("${VIP}_random_test" "${VIP}_ooo_test")
      FIXED_SEEDS=() ;;  # random seeds generated below
  L4) TESTS=("${VIP}_stress_test" "${VIP}_corner_test")
      FIXED_SEEDS=() ;;
  L5) TESTS=("${VIP}_smoke_test" "${VIP}_write_test" "${VIP}_read_test"
             "${VIP}_burst_test" "${VIP}_backpressure_test" "${VIP}_reset_test"
             "${VIP}_error_test" "${VIP}_random_test" "${VIP}_stress_test")
      FIXED_SEEDS=() ;;
  *)  fail "Unknown tier: ${TIER} — use L0 L1 L2 L3 L4 L5"; exit 1 ;;
esac

# ── Generate seeds ─────────────────────────────────────────────────────────────
if [ ${#FIXED_SEEDS[@]} -gt 0 ]; then
  SEEDS=("${FIXED_SEEDS[@]}")
else
  SEEDS=()
  for i in $(seq 1 "${SEED_COUNT}"); do
    SEEDS+=($((RANDOM * RANDOM % 2147483647 + 1)))
  done
fi

# ── Run tests ──────────────────────────────────────────────────────────────────
TOTAL=0; PASSED=0; FAILED=0; NV=0
declare -a FAILURES=()

for TEST in "${TESTS[@]}"; do
  for SEED in "${SEEDS[@]}"; do
    TOTAL=$((TOTAL + 1))
    echo -n "[RUN] ${TEST} seed=${SEED} ... "

    set +e
    ./run.sh "${VIP}" "${TEST}" "${SEED}" 0 UVM_MEDIUM \
      > "${REGDB_DIR}/${TEST}_seed_${SEED}.log" 2>&1
    RUN_EXIT=$?
    set -e

    # Read status from result.json
    RESULT_JSON="results/${VIP}/${TEST}/seed_${SEED}/result.json"
    if [ -f "${RESULT_JSON}" ]; then
      STATUS=$(python3 -c "import json; d=json.load(open('${RESULT_JSON}')); print(d['status'])" 2>/dev/null || echo "NOT_VERIFIED")
    else
      STATUS="NOT_VERIFIED"
    fi

    case "${STATUS}" in
      PASS|EXPECTED_FAILURE_DETECTED)
        echo -e "${GREEN}${STATUS}${NC}"
        PASSED=$((PASSED + 1)) ;;
      NOT_VERIFIED)
        echo -e "${YELLOW}NOT_VERIFIED${NC}"
        NV=$((NV + 1))
        FAILURES+=("${TEST}:seed=${SEED}:NOT_VERIFIED") ;;
      *)
        echo -e "${RED}${STATUS}${NC}"
        FAILED=$((FAILED + 1))
        FAILURES+=("${TEST}:seed=${SEED}:${STATUS}") ;;
    esac
  done
done

# ── Summary ────────────────────────────────────────────────────────────────────
PASS_PCT=0
[ ${TOTAL} -gt 0 ] && PASS_PCT=$(echo "scale=1; ${PASSED}*100/${TOTAL}" | bc)

OVERALL="PASS"
[ ${FAILED} -gt 0 ] && OVERALL="FAIL"
[ ${NV} -gt 0 ]     && OVERALL="FAIL"

# Write summary JSON
cat > "${REGDB_DIR}/summary.json" << EOF
{
  "run_id":     "${RUN_ID}",
  "vip":        "${VIP}",
  "tier":       "${TIER}",
  "timestamp":  "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "commit_sha": "$(git rev-parse HEAD 2>/dev/null || echo UNKNOWN)",
  "total":      ${TOTAL},
  "pass":       ${PASSED},
  "fail":       ${FAILED},
  "not_verified": ${NV},
  "pass_pct":   ${PASS_PCT},
  "status":     "${OVERALL}"
}
EOF

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         REGRESSION SUMMARY — ${TIER}"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Total        : ${TOTAL}"
echo "║  PASS         : ${PASSED}  (${PASS_PCT}%)"
echo "║  FAIL         : ${FAILED}"
echo "║  NOT_VERIFIED : ${NV}"
echo "║  Status       : ${OVERALL}"
echo "╚══════════════════════════════════════════════════════╝"

if [ ${#FAILURES[@]} -gt 0 ]; then
  echo ""
  echo "Failures:"
  for F in "${FAILURES[@]}"; do echo "  ✗ ${F}"; done
fi

echo ""
echo "Summary: ${REGDB_DIR}/summary.json"

if [ "${OVERALL}" = "PASS" ]; then
  pass "STATUS: PASS — ${TIER} regression"
  case "${TIER}" in
    L1) echo "GATE 3: PASS — smoke complete"; echo "NEXT: make regress-l2 VIP=${VIP}" ;;
    L2) echo "GATE 4: PASS — directed complete"; echo "NEXT: make regress-l3 VIP=${VIP}" ;;
    L3) echo "GATE 5: PASS — random complete"; echo "NEXT: Run negative tests" ;;
    L4) echo "GATE 7: candidate met"; echo "NEXT: Check assertions and coverage" ;;
    L5) echo "GATE 9: candidate met"; echo "NEXT: Independent review required for GATE 10" ;;
  esac
else
  fail "STATUS: FAIL — ${TIER} regression"
  echo "NEXT: Debug failures — ./run.sh ${VIP} <failing_test> <seed> 1"
fi
echo ""
