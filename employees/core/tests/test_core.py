"""Tests for the shared loop.

Standard library only, so they run wherever Python does — including here, where
pytest is not installed:

    python -m unittest discover -s employees/core/tests -t .
"""

from __future__ import annotations

import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from employees.core import (  # noqa: E402
    Allowlist, ArtifactInvalid, BlastRadiusViolation, Budget, BudgetExceeded,
    CoreError, LivenessExceeded, Redactor, RetriesExhausted, Run,
    SensitiveDataInInput, call_with_retry, canonical, find_credentials,
    fingerprint, validate, write_atomic,
)

SPEC = Path(__file__).resolve().parents[2] / "keystone" / "EMPLOYEE.md"

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "gaps", "verdict_effect"],
    "properties": {
        "status": {"type": "string", "enum": ["ok", "partial", "failed", "escalated"]},
        "gaps": {"type": "array", "items": {"type": "string"}},
        "verdict_effect": {"const": "none"},
        "count": {"type": "integer"},
    },
}
GOOD = {"status": "ok", "gaps": [], "verdict_effect": "none", "count": 3}


def a_budget(**kw) -> Budget:
    defaults = dict(
        tokens_max=1000, tool_calls_max=5, usd_cap=1.0, liveness_seconds=60,
        prices={"claude-opus-5": (5.0, 25.0)},
    )
    defaults.update(kw)
    return Budget(**defaults)


class TestBudget(unittest.TestCase):
    def test_projects_before_the_call_and_refuses_a_breach(self):
        b = a_budget()
        b.project(model="claude-opus-5", tokens_in=100, tokens_out=100)
        self.assertEqual(b.tokens_used, 0, "projection must not spend")
        with self.assertRaises(BudgetExceeded) as ctx:
            b.project(tokens_in=2000)
        self.assertIn("budget_breach:tokens", ctx.exception.reason)
        self.assertEqual(ctx.exception.status, "failed")

    def test_tool_calls_and_usd_have_their_own_ceilings(self):
        b = a_budget(tool_calls_max=1)
        b.spend(tool_calls=1)
        with self.assertRaises(BudgetExceeded) as ctx:
            b.project(tool_calls=1)
        self.assertIn("tool_calls", ctx.exception.reason)

        # Ceilings are checked cheapest first, so isolating the USD one needs
        # headroom on the others; otherwise tokens breaches before cost is priced.
        b2 = a_budget(usd_cap=0.001, tokens_max=2_000_000, tool_calls_max=10)
        with self.assertRaises(BudgetExceeded) as ctx:
            b2.project(model="claude-opus-5", tokens_in=1_000_000)
        self.assertIn("usd", ctx.exception.reason)

    def test_an_unpriced_model_costs_nothing_and_is_reported(self):
        b = a_budget(prices={})
        self.assertFalse(b.priced)
        self.assertEqual(b.estimate("claude-opus-5", 1_000_000, 0), 0.0)

    def test_liveness_deadline(self):
        b = a_budget(liveness_seconds=0)
        with self.assertRaises(LivenessExceeded):
            b.check_liveness()

    def test_regeneration_cap(self):
        b = a_budget(max_regenerations=2)
        b.regenerate()
        b.regenerate()
        with self.assertRaises(BudgetExceeded):
            b.regenerate()


class TestRetry(unittest.TestCase):
    def test_four_attempts_then_gives_up(self):
        attempts = []

        def flaky():
            attempts.append(1)
            raise TimeoutError("boom")

        with self.assertRaises(RetriesExhausted):
            call_with_retry(flaky, sleep=lambda _: None, rng=random.Random(0))
        self.assertEqual(len(attempts), 4)

    def test_succeeds_after_a_transient_failure(self):
        state = {"n": 0}

        def sometimes():
            state["n"] += 1
            if state["n"] < 3:
                raise ConnectionError("reset")
            return "done"

        self.assertEqual(
            call_with_retry(sometimes, sleep=lambda _: None, rng=random.Random(0)), "done"
        )

    def test_never_retries_a_decision(self):
        calls = []

        def breaches():
            calls.append(1)
            raise BudgetExceeded("ceiling")

        with self.assertRaises(BudgetExceeded):
            call_with_retry(breaches, sleep=lambda _: None)
        self.assertEqual(len(calls), 1, "a budget breach must not be retried")


class TestRedaction(unittest.TestCase):
    def test_masks_env_values_anywhere_including_nested(self):
        env = {"TOKEN": "s3cret-value-long-enough"}
        r = Redactor(["TOKEN"], environ=env)
        out = r.scrub({"msg": "using s3cret-value-long-enough now", "xs": ["s3cret-value-long-enough"]})
        self.assertNotIn("s3cret-value-long-enough", json.dumps(out))
        self.assertIn("***", out["msg"])

    def test_masks_credential_shapes_never_seen_in_the_environment(self):
        r = Redactor([])
        self.assertNotIn("ghp_", r.scrub("token ghp_" + "a" * 24))

    def test_short_values_are_not_masked(self):
        r = Redactor(["SHORT"], environ={"SHORT": "ab"})
        self.assertEqual(r.scrub("ab cd"), "ab cd")

    def test_find_credentials_returns_kinds_not_values(self):
        secret = "sk-ant-" + "b" * 24
        kinds = find_credentials(f"leaked {secret}")
        self.assertEqual(kinds, ["anthropic_api_key"])
        self.assertNotIn(secret, "".join(kinds))


class TestAllowlist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_read_only_is_the_default(self):
        al = Allowlist([self.root / "reports"], apply=False, base=self.root)
        with self.assertRaises(BlastRadiusViolation) as ctx:
            al.assert_writable(self.root / "reports" / "x.json")
        self.assertEqual(ctx.exception.reason, "dry_run_write_attempt")

    def test_apply_permits_only_the_allowlist(self):
        al = Allowlist([self.root / "reports"], apply=True, base=self.root)
        al.assert_writable(self.root / "reports" / "x.json")
        with self.assertRaises(BlastRadiusViolation) as ctx:
            al.assert_writable(self.root / "skills" / "SKILL.md")
        self.assertIn("blast_radius_violation", ctx.exception.reason)

    def test_traversal_cannot_climb_out_by_spelling(self):
        al = Allowlist([self.root / "reports"], apply=True, base=self.root)
        with self.assertRaises(BlastRadiusViolation):
            al.assert_writable(self.root / "reports" / ".." / "etc" / "override.md")

    def test_input_paths_are_resolved_against_their_roots(self):
        al = Allowlist([], apply=False, base=self.root)
        with self.assertRaises(BlastRadiusViolation) as ctx:
            al.assert_readable(self.root / "in" / ".." / ".." / "etc" / "passwd",
                               roots=[self.root / "in"])
        self.assertEqual(ctx.exception.reason, "path_traversal_rejected")


class TestArtifact(unittest.TestCase):
    def test_accepts_a_conforming_instance(self):
        self.assertTrue(validate(GOOD, SCHEMA).valid)

    def test_catches_the_constraints_these_schemas_rely_on(self):
        for bad, expect in [
            ({"status": "ok", "gaps": []}, "required"),
            ({**GOOD, "extra": 1}, "additional"),
            ({**GOOD, "verdict_effect": "changed"}, "const"),
            ({**GOOD, "status": "clean"}, "one of"),
            ({**GOOD, "count": "three"}, "integer"),
        ]:
            with self.subTest(expect=expect):
                result = validate(bad, SCHEMA)
                self.assertFalse(result.valid)
                self.assertTrue(any(expect in e for e in result.errors), result.errors)

    def test_reports_which_validator_ran(self):
        result = validate(GOOD, SCHEMA)
        self.assertIn(result.validator, {"jsonschema", "structural-fallback"})
        self.assertEqual(result.complete, result.validator == "jsonschema")

    def test_canonical_form_is_order_independent(self):
        self.assertEqual(canonical({"b": 1, "a": 2}), canonical({"a": 2, "b": 1}))
        self.assertTrue(canonical({}).endswith("\n"))

    def test_fingerprint_is_stable_and_order_sensitive(self):
        self.assertEqual(fingerprint("a", "b"), fingerprint("a", "b"))
        self.assertNotEqual(fingerprint("a", "b"), fingerprint("b", "a"))

    def test_write_atomic_leaves_no_temporary_behind(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "sub" / "out.json"
            sha = write_atomic(target, '{"a":1}\n')
            self.assertEqual(target.read_text(), '{"a":1}\n')
            self.assertEqual(len(sha), 64)
            self.assertEqual([p.name for p in target.parent.iterdir()], ["out.json"])


class TestRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def a_run(self, *, apply=True, **kw) -> Run:
        return Run(
            employee="keystone", version="1.0.1", model="claude-opus-5",
            spec_path=SPEC, trigger_kind="manual", budget=a_budget(),
            allowlist=Allowlist([self.root / "reports"], apply=apply, base=self.root),
            runs_root=self.root / "runs", **kw,
        )

    def last_record(self) -> dict:
        records = sorted((self.root / "runs").rglob("*.record.json"))
        self.assertTrue(records, "a record must be written for every run")
        return json.loads(records[-1].read_text())

    def test_a_clean_run_is_ok_and_writes_its_artifact(self):
        with self.a_run() as run:
            run.emit(self.root / "reports" / "r.json", GOOD, SCHEMA)
        rec = self.last_record()
        # Only degraded validation may add a gap; with none, the run is ok.
        self.assertIn(rec["status"], {"ok", "partial"})
        self.assertEqual(len(rec["artifacts"]), 1)
        self.assertTrue((self.root / "reports" / "r.json").exists())

    def test_a_gap_keeps_a_run_off_ok(self):
        with self.a_run() as run:
            run.gap("catalog-missing:dv.pipeline")
        self.assertEqual(self.last_record()["status"], "partial")

    def test_an_escalation_outranks_a_gap(self):
        with self.a_run() as run:
            run.gap("something")
            run.escalate("mandate_conflict", "a human must choose")
        rec = self.last_record()
        self.assertEqual(rec["status"], "escalated")
        self.assertEqual(rec["escalations"][0]["reason"], "mandate_conflict")

    def test_an_invalid_artifact_is_never_written_and_the_run_fails(self):
        target = self.root / "reports" / "bad.json"
        with self.a_run() as run:
            run.emit(target, {"status": "ok"}, SCHEMA)
        self.assertFalse(target.exists(), "an invalid artifact must not reach its path")
        rec = self.last_record()
        self.assertEqual(rec["status"], "failed")
        self.assertEqual(rec["escalations"][0]["reason"], "artifact_schema_invalid")

    def test_a_dry_run_validates_but_writes_nothing(self):
        target = self.root / "reports" / "dry.json"
        with self.a_run(apply=False) as run:
            self.assertIsNone(run.emit(target, GOOD, SCHEMA))
        self.assertFalse(target.exists())
        self.assertEqual(self.last_record()["artifacts"], [])

    def test_a_credential_in_an_input_halts_without_recording_the_value(self):
        secret = "ghp_" + "c" * 24
        with self.a_run() as run:
            run.guard_input("skills/dv/SKILL.md", f"description: {secret}")
        rec = self.last_record()
        self.assertEqual(rec["status"], "escalated")
        self.assertNotIn(secret, json.dumps(rec))
        self.assertIn("sensitive_data_in_input", json.dumps(rec))

    def test_a_budget_breach_ends_the_run_failed_with_a_record(self):
        with self.a_run() as run:
            run.budget.project(tokens_in=10_000)
        rec = self.last_record()
        self.assertEqual(rec["status"], "failed")
        self.assertIn("budget_breach", json.dumps(rec["escalations"]))
        self.assertEqual(rec["budget"]["tokens_max"], 1000)

    def test_the_record_carries_the_specification_it_ran(self):
        with self.a_run():
            pass
        rec = self.last_record()
        self.assertEqual(len(rec["prompt_sha"]), 64)
        self.assertEqual(rec["employee"], "keystone")
        self.assertTrue(rec["trace_path"].endswith(".jsonl"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
