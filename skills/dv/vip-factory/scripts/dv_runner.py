#!/usr/bin/env python3
"""
AVIK VIP Factory — DV Runner
Unified execution interface for compile, simulate, regress, and report.
Never claims PASS without observable simulator evidence.
"""

import subprocess
import json
import os
import sys
import random
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

# ─── Constants ────────────────────────────────────────────────────────────────

VALID_STATUSES = {
    "PASS", "FAIL", "NOT_VERIFIED", "BLOCKED",
    "EXPECTED_FAILURE_DETECTED", "UNEXPECTED_PASS"
}

# ─── Result Schema ─────────────────────────────────────────────────────────────

def make_result(test: str, seed: int, status: str = "NOT_VERIFIED",
                exit_code: int = -1, **kwargs) -> dict:
    """
    Create a canonical result record.
    Default status is NOT_VERIFIED — must be explicitly set to PASS.
    """
    assert status in VALID_STATUSES, f"Invalid status: {status}"
    return {
        "test":                 test,
        "seed":                 seed,
        "simulator":            "verilator",
        "simulator_version":    get_verilator_version(),
        "commit_sha":           get_git_sha(),
        "timestamp":            datetime.utcnow().isoformat(),
        "status":               status,
        "exit_code":            exit_code,
        "uvm_errors":           kwargs.get("uvm_errors", -1),
        "uvm_fatals":           kwargs.get("uvm_fatals", -1),
        "assertion_failures":   kwargs.get("assertion_failures", -1),
        "scoreboard_errors":    kwargs.get("scoreboard_errors", -1),
        "functional_coverage":  kwargs.get("functional_coverage", 0.0),
        "code_coverage":        kwargs.get("code_coverage", 0.0),
        "runtime_seconds":      kwargs.get("runtime_seconds", 0.0),
        "expected":             kwargs.get("expected", "NORMAL"),
        "observed":             kwargs.get("observed", "UNKNOWN"),
        "waveform":             kwargs.get("waveform", ""),
        "notes":                kwargs.get("notes", ""),
    }

# ─── Environment ──────────────────────────────────────────────────────────────

def get_verilator_version() -> str:
    try:
        r = subprocess.run(["verilator", "--version"], capture_output=True, text=True)
        return r.stdout.strip().split("\n")[0]
    except Exception:
        return "UNKNOWN"

def get_git_sha() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return "UNKNOWN"

def check_environment() -> bool:
    """Verify all required tools are present."""
    tools = ["verilator", "python3", "git"]
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        print(f"[BLOCKED] Missing tools: {missing}")
        print("Install: sudo apt-get install -y verilator python3 git")
        return False
    print(f"[ENV] Verilator: {get_verilator_version()}")
    return True

# ─── Compile ──────────────────────────────────────────────────────────────────

def compile_vip(vip: str, extra_flags: list = None) -> dict:
    """
    Compile the VIP testbench using Verilator.
    Returns compile result — NEVER infers simulation result from compile.
    """
    vip_dir = Path(f"vip/{vip}")
    filelist = vip_dir / "tb" / "filelist.f"

    if not filelist.exists():
        return {"status": "BLOCKED", "reason": f"filelist.f not found: {filelist}"}

    obj_dir = Path(f"obj_dir/{vip}")
    obj_dir.mkdir(parents=True, exist_ok=True)

    flags = [
        "verilator", "--sv", "--binary",
        "-DUVM_NO_DPI",
        "--coverage",
        "--trace-fst",
        "-j", "4",
        f"-f", str(filelist),
        "-top", "tb_top",
        f"-o", f"obj_dir/{vip}/simv",
        f"--Mdir", f"obj_dir/{vip}",
    ] + (extra_flags or [])

    log_path = Path(f"logs/{vip}_compile.log")
    log_path.parent.mkdir(exist_ok=True)

    print(f"[COMPILE] {vip} ...")
    result = subprocess.run(flags, capture_output=True, text=True)
    log_path.write_text(result.stdout + result.stderr)

    if result.returncode != 0:
        print(f"[COMPILE FAIL] See {log_path}")
        return {"status": "FAIL", "exit_code": result.returncode, "log": str(log_path)}

    print(f"[COMPILE PASS] {vip}")
    return {"status": "PASS", "exit_code": 0, "log": str(log_path)}

# ─── Simulate ─────────────────────────────────────────────────────────────────

def run_test(vip: str, test: str, seed: int,
             expected: str = "NORMAL",
             timeout_sec: int = 300,
             dump_waves: bool = False) -> dict:
    """
    Run a single simulation. Parse results from log.
    NEVER declares PASS without parsing the simulator output.
    """
    simv = Path(f"obj_dir/{vip}/simv")
    if not simv.exists():
        return make_result(test, seed, status="BLOCKED",
                          notes=f"simv not found — compile first: {simv}")

    result_dir = Path(f"results/{vip}/{test}/seed_{seed}")
    result_dir.mkdir(parents=True, exist_ok=True)

    log_path    = result_dir / "transcript.log"
    wave_path   = result_dir / "waveform.fst"
    result_path = result_dir / "result.json"

    cmd = [
        str(simv),
        f"+UVM_TESTNAME={test}",
        "+UVM_VERBOSITY=UVM_MEDIUM",
        f"+ntb_random_seed={seed}",
    ]
    if dump_waves:
        cmd += ["+DUMP_WAVES=1", f"+WAVE_FILE={wave_path}"]

    print(f"[RUN] {test} seed={seed} ...", end=" ", flush=True)
    t_start = datetime.utcnow()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        runtime = (datetime.utcnow() - t_start).total_seconds()
        log_text = proc.stdout + proc.stderr
        log_path.write_text(log_text)

        # Parse result — never infer PASS from exit code alone
        parsed = parse_log(log_text, proc.returncode, expected)
        parsed["runtime_seconds"] = runtime
        parsed["waveform"] = str(wave_path) if dump_waves else ""

    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        parsed = {"status": "FAIL", "uvm_errors": -1, "uvm_fatals": -1,
                  "assertion_failures": -1, "scoreboard_errors": -1,
                  "functional_coverage": 0.0, "code_coverage": 0.0,
                  "runtime_seconds": timeout_sec, "expected": expected,
                  "observed": "TIMEOUT", "notes": "Simulation timed out"}

    result = make_result(test, seed, **parsed)
    result_path.write_text(json.dumps(result, indent=2))
    print(result["status"])
    return result

# ─── Log Parser (truth authority) ─────────────────────────────────────────────

def parse_log(log: str, exit_code: int, expected: str = "NORMAL") -> dict:
    """
    Parse simulator log to determine status.
    This is the ONLY function that may set status = PASS.
    """
    # Extract UVM report summary
    uvm_errors   = extract_uvm_count(log, "UVM_ERROR")
    uvm_fatals   = extract_uvm_count(log, "UVM_FATAL")
    assert_fails = extract_assertion_failures(log)
    sb_errors    = extract_scoreboard_errors(log)

    # Determine what was observed
    if uvm_fatals > 0:
        observed = "UVM_FATAL"
    elif uvm_errors > 0:
        observed = f"UVM_ERROR_x{uvm_errors}"
    elif assert_fails > 0:
        observed = f"ASSERTION_FAIL_x{assert_fails}"
    elif sb_errors > 0:
        observed = f"SCOREBOARD_ERROR_x{sb_errors}"
    elif "PROTOCOL_VIOLATION" in log or "PROTOCOL_ERROR" in log:
        observed = "PROTOCOL_VIOLATION"
    elif exit_code == 0 and "UVM_ERROR :    0" in log and "UVM_FATAL :    0" in log:
        observed = "NORMAL"
    else:
        observed = "UNKNOWN"

    # Determine status based on expected vs observed
    if expected == "NORMAL":
        if (observed == "NORMAL" and
                exit_code == 0 and
                uvm_errors == 0 and
                uvm_fatals == 0 and
                assert_fails == 0 and
                sb_errors == 0):
            status = "PASS"
        else:
            status = "FAIL"

    elif expected in ("PROTOCOL_ERROR", "PROTOCOL_VIOLATION"):
        if observed == "PROTOCOL_VIOLATION":
            status = "EXPECTED_FAILURE_DETECTED"
        elif observed == "NORMAL":
            status = "UNEXPECTED_PASS"  # checker missed it = FAIL
        else:
            status = "FAIL"

    else:
        status = "NOT_VERIFIED"

    return {
        "status":             status,
        "exit_code":          exit_code,
        "uvm_errors":         uvm_errors,
        "uvm_fatals":         uvm_fatals,
        "assertion_failures": assert_fails,
        "scoreboard_errors":  sb_errors,
        "functional_coverage": extract_coverage(log),
        "code_coverage":      0.0,
        "expected":           expected,
        "observed":           observed,
    }

def extract_uvm_count(log: str, keyword: str) -> int:
    """Extract UVM error/fatal count from report summary line."""
    import re
    # Look for "UVM_ERROR : N" in the report summary
    pattern = rf"{keyword}\s*:\s*(\d+)"
    matches = re.findall(pattern, log)
    if matches:
        # Take the last occurrence (report summary is at end)
        return int(matches[-1])
    # If no summary found and keyword appears in log body — assume at least 1
    if keyword in log:
        return -1  # Unknown count — cannot claim PASS
    return 0

def extract_assertion_failures(log: str) -> int:
    import re
    m = re.search(r"ASSERTION_FAILURES\s*:\s*(\d+)", log)
    return int(m.group(1)) if m else (1 if "Assertion failed" in log else 0)

def extract_scoreboard_errors(log: str) -> int:
    import re
    m = re.search(r"SCOREBOARD_ERRORS\s*:\s*(\d+)", log)
    if m:
        return int(m.group(1))
    return log.count("SCOREBOARD ERROR") + log.count("MISMATCH")

def extract_coverage(log: str) -> float:
    import re
    m = re.search(r"Functional coverage:\s*([\d.]+)%", log)
    return float(m.group(1)) if m else 0.0

# ─── Regression ───────────────────────────────────────────────────────────────

def run_regression(vip: str, tier: str, seeds: list = None) -> dict:
    """Run a regression tier and return aggregated summary."""
    tier_tests = get_tier_tests(vip, tier)
    if not tier_tests:
        return {"status": "BLOCKED", "reason": f"No tests found for {vip} tier {tier}"}

    if seeds is None:
        if tier == "L1":
            seeds = [1, 2, 3]
        elif tier == "L2":
            seeds = list(range(1, 11))
        elif tier == "L3":
            seeds = [random.randint(1, 2**31) for _ in range(100)]
        else:
            seeds = [random.randint(1, 2**31) for _ in range(1000)]

    results = []
    for test in tier_tests:
        for seed in seeds:
            r = run_test(vip, test, seed)
            results.append(r)

    return generate_summary(vip, tier, results)

def get_tier_tests(vip: str, tier: str) -> list:
    """Return test list for a given tier."""
    test_dir = Path(f"vip/{vip}/tests")
    if not test_dir.exists():
        return []
    tier_map = {
        "L1": ["smoke"],
        "L2": ["write", "read", "burst", "backpressure", "reset", "error"],
        "L3": ["random", "ooo"],
        "L4": ["stress", "corner"],
        "L5": None,  # all tests
    }
    patterns = tier_map.get(tier, [])
    if patterns is None:
        return [f.stem for f in test_dir.glob("*_test.sv")]
    return [f.stem for f in test_dir.glob("*_test.sv")
            if any(p in f.stem for p in patterns)]

def generate_summary(vip: str, tier: str, results: list) -> dict:
    total   = len(results)
    passed  = sum(1 for r in results if r["status"] in ("PASS", "EXPECTED_FAILURE_DETECTED"))
    failed  = sum(1 for r in results if r["status"] in ("FAIL", "UNEXPECTED_PASS"))
    nv      = sum(1 for r in results if r["status"] == "NOT_VERIFIED")
    pass_pct = round(100 * passed / total, 1) if total else 0

    summary = {
        "vip":       vip,
        "tier":      tier,
        "timestamp": datetime.utcnow().isoformat(),
        "commit_sha": get_git_sha(),
        "total":     total,
        "pass":      passed,
        "fail":      failed,
        "not_verified": nv,
        "pass_pct":  pass_pct,
        "status":    "PASS" if failed == 0 and nv == 0 else "FAIL",
        "failures":  [r for r in results if r["status"] not in ("PASS", "EXPECTED_FAILURE_DETECTED")],
    }

    # Save summary
    run_id   = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    sum_path = Path(f"regression_db/runs/{run_id}_{vip}_{tier}/summary.json")
    sum_path.parent.mkdir(parents=True, exist_ok=True)
    sum_path.write_text(json.dumps(summary, indent=2))

    print(f"\n{'='*50}")
    print(f"  {vip} {tier} REGRESSION SUMMARY")
    print(f"{'='*50}")
    print(f"  Total        : {total}")
    print(f"  PASS         : {passed}  ({pass_pct}%)")
    print(f"  FAIL         : {failed}")
    print(f"  NOT_VERIFIED : {nv}")
    print(f"  Status       : {summary['status']}")
    print(f"{'='*50}\n")
    return summary

# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVIK VIP Factory DV Runner")
    parser.add_argument("command", choices=["compile", "run", "regress", "env"])
    parser.add_argument("--vip",   required=False)
    parser.add_argument("--test",  required=False)
    parser.add_argument("--seed",  type=int, default=1)
    parser.add_argument("--tier",  default="L1")
    parser.add_argument("--waves", action="store_true")
    args = parser.parse_args()

    if args.command == "env":
        ok = check_environment()
        sys.exit(0 if ok else 1)

    if args.command == "compile":
        r = compile_vip(args.vip)
        sys.exit(0 if r["status"] == "PASS" else 1)

    if args.command == "run":
        r = run_test(args.vip, args.test, args.seed, dump_waves=args.waves)
        print(json.dumps(r, indent=2))
        sys.exit(0 if r["status"] == "PASS" else 1)

    if args.command == "regress":
        r = run_regression(args.vip, args.tier)
        sys.exit(0 if r["status"] == "PASS" else 1)
