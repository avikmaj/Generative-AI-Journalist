"""Generate the DV fixtures BLOODHOUND and CARTOGRAPHER run against.

The fixtures are not hand-written JSON. They are produced by driving the real
UVM Verification Studio code — ``classify_uvm_run``, ``RegressionDB``,
``build_report`` and ``VerilatorCoverageReader`` — over simulation logs and a
coverage database written in the formats those modules actually parse. What
lands in ``employees/*/fixtures/`` is therefore the platform's own output, and
a change to the platform's verdict logic changes the fixtures rather than
silently diverging from them.

The logs cover the whole classification space on purpose, including the two
adversarial cases the platform's red team found (RT-P-002, RT-P-007/008), so
that an employee consuming them is exercised against evidence tampering and
not only against tidy failures.

Usage:
    python scripts/make_dv_fixtures.py [--studio-src PATH]

``--studio-src`` points at the platform checkout's ``src`` directory. Without
it the script exits non-zero and writes nothing: fixtures derived from a stub
would be worse than no fixtures.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STUDIO_SRC = Path("/home/user/verification_studio_platform_repo/src")

# Verilator writes coverage records as a \x01key\x02value stream. Reproduced
# here rather than imported, because writing the database is what a simulator
# does; the platform only ever reads it.
KEY, VAL = "\x01", "\x02"

TB = "tb/apb_pkg.sv"
CG = "v_covergroup/cg_apb"


# -- simulation logs -------------------------------------------------------
def _summary(info: int, warning: int, error: int, fatal: int) -> str:
    """An Accellera UVM report summary block, as the library prints it."""
    return (
        "--- UVM Report Summary ---\n"
        "\n"
        "** Report counts by severity\n"
        f"UVM_INFO :{info:5d}\n"
        f"UVM_WARNING :{warning:5d}\n"
        f"UVM_ERROR :{error:5d}\n"
        f"UVM_FATAL :{fatal:5d}\n"
    )


def _preamble(test: str, seed: int) -> str:
    return (
        f"UVM_INFO @ 0: reporter [RNTST] Running test {test}...\n"
        f"UVM_INFO {TB}(198) @ 0: uvm_test_top [CFG] seed={seed} "
        f"backend=verilator uvm=2020.3.1\n"
        f"UVM_INFO {TB}(210) @ 0: uvm_test_top.env.agent.driver [DRV] "
        f"reset released, starting sequence\n"
    )


def _finish(line: int = 96) -> str:
    return f"- tb/tb_top.sv:{line}: Verilog $finish\n"


def clean_pass(test: str, seed: int, transactions: int) -> str:
    return (
        _preamble(test, seed)
        + f"UVM_INFO {TB}(402) @ {transactions * 20}: uvm_test_top.env.sb "
          f"[SB] {transactions} transactions checked, 0 mismatches\n"
        + _summary(transactions + 3, 0, 0, 0)
        + _finish()
    )


def scoreboard_mismatch(test: str, seed: int, addr: str, expected: str) -> str:
    """A real data-integrity failure. Two seeds differing only in address and
    payload must normalise to one signature, which is what makes clustering
    worth doing."""
    return (
        _preamble(test, seed)
        + f"UVM_ERROR {TB}(455) @ 1240: uvm_test_top.env.sb [SB_MISMATCH] "
          f"read data mismatch at addr {addr}: expected {expected}, got 0x00000000\n"
        + _summary(31, 0, 1, 0)
        + _finish()
    )


def clean_but_unfinished(test: str, seed: int) -> str:
    """RT-P-002: a clean summary with no $finish is NOT_VERIFIED, never PASS.
    The run did not end in an orderly way, so nothing about it is established."""
    return (
        _preamble(test, seed)
        + f"UVM_INFO {TB}(402) @ 8800: uvm_test_top.env.sb [SB] "
          f"440 transactions checked, 0 mismatches\n"
        + _summary(443, 0, 0, 0)
    )


def forged_summary(test: str, seed: int) -> str:
    """RT-P-007 / RT-P-008: a genuine summary reporting two errors, followed by
    an appended block reporting zero. Taking the last write would call this a
    pass; taking the maximum calls it what it is."""
    return (
        _preamble(test, seed)
        + f"UVM_ERROR {TB}(455) @ 980: uvm_test_top.env.sb [SB_MISMATCH] "
          f"read data mismatch at addr 0x00000024: expected 0x5A5A5A5A, "
          f"got 0x00000000\n"
        + f"UVM_ERROR {TB}(461) @ 1500: uvm_test_top.env.sb [SB_ORDER] "
          f"response received out of order\n"
        + _summary(22, 0, 2, 0)
        + _finish()
        + _summary(22, 0, 0, 0)
    )


def negative_detected(test: str, seed: int) -> str:
    """The pslverr test: the violation firing IS the pass criterion."""
    return (
        _preamble(test, seed)
        + f"UVM_ERROR {TB}(488) @ 640: uvm_test_top.env.sb [SB_PSLVERR] "
          f"PSLVERR asserted for address 0x00000100 outside the mapped region\n"
        + _summary(18, 0, 1, 0)
        + _finish()
    )


def negative_missed(test: str, seed: int) -> str:
    """The same negative test where nothing fired — the DUT failed to flag an
    illegal access, and a green log is the symptom."""
    return (
        _preamble(test, seed)
        + f"UVM_INFO {TB}(402) @ 640: uvm_test_top.env.sb [SB] "
          f"32 transactions checked, 0 mismatches\n"
        + _summary(35, 0, 0, 0)
        + _finish()
    )


def assertion_failure(test: str, seed: int) -> str:
    return (
        _preamble(test, seed)
        + "%Error: tb/apb_if.sv:64: Assertion failed in "
          "top.tb_top.u_apb_if.ap_pready_stable: PREADY deasserted "
          "before PENABLE fell\n"
        + _summary(9, 0, 0, 0)
    )


# Each entry: test, uvm_testname, tier, seed, expect, log text.
RUNS = [
    ("apb_smoke_test", "apb_smoke_test", "L0", 1, "PASS",
     clean_pass("apb_smoke_test", 1, 24)),
    ("apb_random_test", "apb_random_test", "L1", 1, "PASS",
     clean_pass("apb_random_test", 1, 512)),
    ("apb_random_test", "apb_random_test", "L1", 2, "PASS",
     scoreboard_mismatch("apb_random_test", 2, "0x00000040", "0xDEADBEEF")),
    ("apb_random_test", "apb_random_test", "L1", 3, "PASS",
     scoreboard_mismatch("apb_random_test", 3, "0x0000007C", "0xCAFEBABE")),
    ("apb_random_test", "apb_random_test", "L1", 4, "PASS",
     clean_but_unfinished("apb_random_test", 4)),
    ("apb_random_test", "apb_random_test", "L1", 5, "PASS",
     forged_summary("apb_random_test", 5)),
    ("apb_error_test", "apb_error_test", "L2", 1, "FAIL",
     negative_detected("apb_error_test", 1)),
    ("apb_error_test", "apb_error_test", "L2", 2, "FAIL",
     negative_missed("apb_error_test", 2)),
    ("apb_smoke_test", "apb_smoke_test", "L0", 2, "PASS",
     assertion_failure("apb_smoke_test", 2)),
]

# Runs whose log carries the simulator's own error lines, which a backend
# extracts from its native format before the verdict is taken.
TOOL_ERRORS = {
    ("apb_smoke_test", 2): [
        "%Error: tb/apb_if.sv:64: Assertion failed in "
        "top.tb_top.u_apb_if.ap_pready_stable: PREADY deasserted "
        "before PENABLE fell"
    ],
}

RETURNCODES = {("apb_smoke_test", 2): 1}


# -- coverage database -----------------------------------------------------
def _cg_record(coverpoint: str, bin_name: str, line: int) -> str:
    hier = f"tb_top.u_env.u_cov.cg_apb.{coverpoint}.{bin_name}"
    return (
        f"{KEY}t{VAL}covergroup{KEY}page{VAL}{CG}{KEY}f{VAL}{TB}"
        f"{KEY}l{VAL}{line}{KEY}n{VAL}0{KEY}bin{VAL}{bin_name}{KEY}h{VAL}{hier}"
    )


def _code_record(kind: str, file: str, line: int, comment: str) -> str:
    return (
        f"{KEY}t{VAL}{kind}{KEY}page{VAL}v_{kind}/{Path(file).stem}"
        f"{KEY}f{VAL}{file}{KEY}l{VAL}{line}{KEY}n{VAL}0{KEY}o{VAL}{comment}"
        f"{KEY}h{VAL}top.tb_top.u_dut"
    )


# The bins golden_apb's cg_apb actually declares, with the line each is on in
# tb/apb_pkg.sv. Counts of 0 are the holes.
COVERGROUP_BINS = [
    # cp_dir
    ("cp_dir", "rd", 343, 2104), ("cp_dir", "wr", 344, 2456),
    # cp_resp
    ("cp_resp", "okay", 348, 4368), ("cp_resp", "err", 349, 192),
    # cp_addr
    ("cp_addr", "first_word", 353, 88), ("cp_addr", "low", 354, 1420),
    ("cp_addr", "mid", 355, 2831), ("cp_addr", "last_word", 356, 29),
    ("cp_addr", "err_region", 357, 0),
    # cp_strb
    ("cp_strb", "byte0", 361, 604), ("cp_strb", "byte3", 362, 588),
    ("cp_strb", "halfword", 363, 611), ("cp_strb", "fullword", 364, 640),
    ("cp_strb", "others", 365, 13),
    # cp_wdata_corner
    ("cp_wdata_corner", "zero", 369, 41), ("cp_wdata_corner", "allones", 370, 0),
    ("cp_wdata_corner", "other", 371, 2415),
    # x_dir_resp
    ("x_dir_resp", "<rd,okay>", 384, 2016), ("x_dir_resp", "<rd,err>", 384, 88),
    ("x_dir_resp", "<wr,okay>", 384, 2352), ("x_dir_resp", "<wr,err>", 384, 104),
    # x_dir_addr
    ("x_dir_addr", "<rd,first_word>", 385, 40),
    ("x_dir_addr", "<rd,low>", 385, 655),
    ("x_dir_addr", "<rd,mid>", 385, 1396),
    ("x_dir_addr", "<rd,last_word>", 385, 13),
    ("x_dir_addr", "<rd,err_region>", 385, 0),
    ("x_dir_addr", "<wr,first_word>", 385, 48),
    ("x_dir_addr", "<wr,low>", 385, 765),
    ("x_dir_addr", "<wr,mid>", 385, 1435),
    ("x_dir_addr", "<wr,last_word>", 385, 16),
    ("x_dir_addr", "<wr,err_region>", 385, 0),
    # x_dir_strb — reads carry no byte strobes, so every read bin here is a
    # structural hole the testbench comments call out. Left unfiltered on
    # purpose: the ignore_bins that would remove them is not expressible on
    # this backend, so closure has to reason about them instead.
    ("x_dir_strb", "<rd,byte0>", 386, 0), ("x_dir_strb", "<rd,byte3>", 386, 0),
    ("x_dir_strb", "<rd,halfword>", 386, 0),
    ("x_dir_strb", "<rd,fullword>", 386, 0),
    ("x_dir_strb", "<rd,others>", 386, 0),
    ("x_dir_strb", "<wr,byte0>", 386, 604),
    ("x_dir_strb", "<wr,byte3>", 386, 588),
    ("x_dir_strb", "<wr,halfword>", 386, 611),
    ("x_dir_strb", "<wr,fullword>", 386, 640),
    ("x_dir_strb", "<wr,others>", 386, 13),
]

# Code coverage, present so that a consumer can be checked for the mistake of
# counting it toward functional closure.
CODE_BINS = [
    ("line", "rtl/apb_slave.sv", 41, "always_ff", 4560),
    ("line", "rtl/apb_slave.sv", 58, "if", 2456),
    ("line", "rtl/apb_slave.sv", 71, "else", 2104),
    ("line", "rtl/apb_slave.sv", 88, "pslverr", 192),
    ("branch", "rtl/apb_slave.sv", 58, "if/else", 2456),
    ("branch", "rtl/apb_slave.sv", 88, "if", 192),
    ("toggle", "rtl/apb_if.sv", 22, "pwdata[31]", 0),
]


def write_coverage_dat(path: Path) -> None:
    lines = ["# SystemC::Coverage-3"]
    for coverpoint, bin_name, line, count in COVERGROUP_BINS:
        lines.append(f"C '{_cg_record(coverpoint, bin_name, line)}' {count}")
    for kind, file, line, comment, count in CODE_BINS:
        lines.append(f"C '{_code_record(kind, file, line, comment)}' {count}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# -- driving the platform --------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--studio-src", type=Path, default=DEFAULT_STUDIO_SRC,
                        help="the platform checkout's src/ directory")
    args = parser.parse_args()

    if not (args.studio_src / "uvmstudio").is_dir():
        print(f"error: no uvmstudio package under {args.studio_src}", file=sys.stderr)
        print("Clone avikmaj/Verification_Studio_platform_repo and pass "
              "--studio-src <checkout>/src.", file=sys.stderr)
        return 2
    sys.path.insert(0, str(args.studio_src))

    from uvmstudio.coverage.model import VerilatorCoverageReader
    from uvmstudio.regression.db import RegressionDB
    from uvmstudio.regression.report import build_report
    from uvmstudio.simulator.base import RunRequest
    from uvmstudio.simulator.uvm_classify import classify_uvm_run

    bloodhound = ROOT / "employees" / "bloodhound" / "fixtures"
    cartographer = ROOT / "employees" / "cartographer" / "fixtures"
    logs = bloodhound / "results"
    for directory in (bloodhound, cartographer):
        if directory.exists():
            shutil.rmtree(directory)
    logs.mkdir(parents=True, exist_ok=True)

    db_path = bloodhound / "regression.sqlite"
    db = RegressionDB(db_path)
    regression_id = db.start_regression(
        name="nightly golden_apb L0-L2", project="golden_apb", tier="L2",
        started_utc="2026-09-19T22:00:00Z", git_commit="fd8270f33c9f367c6cbdd44f0",
        git_branch="main", git_dirty=0, backend="verilator",
        backend_version="5.050", frontend_version="slang 11.0.0",
        uvm_version="2020.3.1", host="uvmstudio-runner",
    )

    for test, uvm_testname, tier, seed, expect, text in RUNS:
        log_path = logs / f"{test}_{seed}.log"
        log_path.write_text(text, encoding="utf-8")

        request = RunRequest(
            binary=Path("build/V" + "tb_top"), run_dir=logs, seed=seed,
            uvm_testname=uvm_testname, timeout_s=900, expect=expect,
        )
        result = classify_uvm_run(
            text=text,
            returncode=RETURNCODES.get((test, seed), 0),
            timed_out=False,
            request=request,
            tool_errors=TOOL_ERRORS.get((test, seed), []),
            tool_label="verilator",
        )
        result.log_path = log_path.relative_to(bloodhound)
        db.record_run(regression_id, result, test=test,
                      uvm_testname=uvm_testname, tier=tier)
        print(f"  {test:16} seed {seed}  {result.status.value}")

    db.finish_regression(regression_id)
    report = build_report(db, regression_id)
    (bloodhound / "report.json").write_text(
        json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")

    summary = report["summary"]
    print(f"\nregression: {summary['status']}  "
          f"PASS={summary['passed']} FAIL={summary['failed']} "
          f"NOT_VERIFIED={summary['not_verified']} total={summary['total']}")
    print(f"clusters:   {len(report['failure_clusters'])}")

    dat = cartographer / "coverage.dat"
    write_coverage_dat(dat)
    coverage = VerilatorCoverageReader().load(dat)
    coverage.sources = ["coverage.dat"]
    (cartographer / "coverage-summary.json").write_text(
        json.dumps(coverage.summary(), indent=2) + "\n", encoding="utf-8")

    covered, total, percent = coverage.functional_score()
    print(f"functional: {covered}/{total} bins = {percent}%  "
          f"holes={len(coverage.holes())}")
    print(f"\nwrote {bloodhound.relative_to(ROOT)} and "
          f"{cartographer.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
