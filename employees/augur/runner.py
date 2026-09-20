"""AUGUR — the weekly analytics read, with the noise held back.

Channel analytics invite two mistakes and AUGUR is built to refuse both.

The first is reading a number that is not finished. YouTube back-fills for
days, so any row inside the lag window is excluded rather than analysed, and
the artifact states how many rows that was. A week read early is not a week
read badly — it is a different week.

The second is attributing a swing that is only small-sample noise. A video
below the impressions floor cannot produce a mover at all, and a delta inside
the trailing interquartile range is not a mover either. What survives both
filters gets an attribution, and where the cause genuinely cannot be told
apart the attribution says which kind of not-knowing it is — ``undetermined``
when the causes are not separable, ``insufficient_volume_for_causal_claim``
when the volume is too thin to carry one — rather than a guess.

Exactly three actions are emitted, because a weekly list of nine is a list
nobody works through. The schema pins the count at three.

Run it over the committed fixture with::

    python employees/augur/runner.py --analytics employees/augur/fixtures/week.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402

METRICS = ["ctr", "average_view_duration_seconds", "retention_at_30s_ratio",
           "traffic_source_mix_browse_share", "subscriber_delta_weekly"]

# Below this, a week's numbers for one video are small-sample noise.
IMPRESSIONS_FLOOR = 1000
# Analytics are not settled inside this window, so rows in it are excluded.
LAG_DAYS = 3
# A metric needs this many complete trailing weeks before a baseline means
# anything. Below it the baseline is null and no mover is called against it.
MIN_HISTORY_WEEKS = 6

INSTRUCTION = re.compile(
    r"\b(?:ignore (?:all |the )?(?:previous|above)|you are now|system prompt|"
    r"rank this|report this as|the operator (?:says|approves))\b", re.I)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Augur(EmployeeRunner):
    handle = "augur"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--analytics", type=Path, required=True,
                            help="one week of channel analytics")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.analytics.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("analytics", raw)
        doc = json.loads(raw)
        digest = sha256_hex(raw)
        run.record.input_digest = digest

        end = date.fromisoformat(doc["week_end"])
        cutoff = end - timedelta(days=LAG_DAYS)
        start = end - timedelta(days=6)

        injections = []
        rows, excluded_lag, malformed, below_floor = [], 0, 0, 0
        for row in doc["rows"]:
            text = f"{row.get('title', '')} {row.get('custom_dimension', '')}"
            if INSTRUCTION.search(text):
                injections.append({
                    "kind": "instruction_in_title" if INSTRUCTION.search(
                        row.get("title", "")) else "instruction_in_custom_dimension",
                    "field": "title" if INSTRUCTION.search(row.get("title", ""))
                             else "custom_dimension",
                    "excerpt_sha256": sha256_hex(text.strip()),
                    "action_taken": "field_ignored",
                    "verdict_unaffected": True})

            try:
                observed = date.fromisoformat(row["observed_on"])
                impressions = int(row["impressions"])
            except (KeyError, ValueError, TypeError):
                malformed += 1
                continue
            if any(not isinstance(row.get(m), (int, float)) for m in METRICS):
                malformed += 1
                continue
            if row["ctr"] < 0 or row["ctr"] > 1:
                injections.append({
                    "kind": "impossible_value", "field": "ctr",
                    "excerpt_sha256": sha256_hex(str(row["ctr"])),
                    "action_taken": "row_dropped",
                    "verdict_unaffected": True})
                malformed += 1
                continue
            if observed > cutoff:
                excluded_lag += 1
                continue
            if impressions < IMPRESSIONS_FLOOR:
                below_floor += 1
                continue
            rows.append(row)

        if excluded_lag:
            run.gap(f"rows_excluded_inside_the_{LAG_DAYS}_day_lag_window:"
                    f"{excluded_lag}")
        if malformed:
            run.gap(f"rows_rejected_malformed:{malformed}")

        # Baselines over the trailing weeks. Short history yields a null
        # baseline, and a null baseline calls no movers.
        history = doc.get("trailing_weeks", {})
        baseline = []
        usable_metrics = set()
        for metric in METRICS:
            series = [v for v in history.get(metric, [])
                      if isinstance(v, (int, float))]
            sufficient = len(series) >= MIN_HISTORY_WEEKS
            if sufficient:
                usable_metrics.add(metric)
                quartiles = statistics.quantiles(series, n=4)
                baseline.append({
                    "metric": metric,
                    "trailing_median": round(statistics.median(series), 4),
                    "trailing_iqr": round(quartiles[2] - quartiles[0], 4),
                    "complete_weeks": len(series), "sufficient_history": True})
            else:
                baseline.append({
                    "metric": metric, "trailing_median": None,
                    "trailing_iqr": None, "complete_weeks": len(series),
                    "sufficient_history": False})
                run.gap(f"insufficient_history:{metric}:{len(series)}_weeks")

        by_metric = {b["metric"]: b for b in baseline}
        movers = []
        severity: dict[tuple[str, str], float] = {}
        for row in rows:
            for metric in METRICS:
                base = by_metric[metric]
                if metric not in usable_metrics:
                    continue
                delta = float(row[metric]) - base["trailing_median"]
                # A swing inside the trailing IQR is the metric being itself.
                if abs(delta) <= max(base["trailing_iqr"], 1e-9):
                    continue
                attribution, confidence = self.attribute(row, metric)
                movers.append({
                    "video_id": row["video_id"], "metric": metric,
                    "delta": round(delta, 4), "attribution": attribution,
                    "attribution_confidence": confidence,
                    "impressions_in_window": int(row["impressions"])})
                # Ranking is by how many trailing IQRs the metric moved, not by
                # the raw delta: +34 seconds and +0.042 CTR are not comparable
                # numbers, and sorting them together would order the list by
                # unit rather than by significance.
                severity[(row["video_id"], metric)] = abs(delta) / max(
                    base["trailing_iqr"], 1e-9)
        movers.sort(key=lambda m: (-severity[(m["video_id"], m["metric"])],
                                   m["video_id"], m["metric"]))

        retention = [
            {"video_id": r["video_id"], "dropoff_s": float(r["dropoff_s"]),
             "hypothesis": r["hypothesis"][:400], "attribution": r["attribution"]}
            for r in doc.get("retention", [])]
        decaying = [
            {"video_id": d["video_id"],
             "impressions_delta": int(d["impressions_delta"]),
             "likely_cause": d["likely_cause"]}
            for d in doc.get("decaying", [])]

        actions = self.actions(movers, retention, decaying)
        review = [{"action": a["action"], "taken": a["taken"],
                   "outcome": a["outcome"]}
                  for a in doc.get("last_week_actions", [])[:3]]

        run.finding(len(movers) + len(retention) + len(decaying))
        deductions = [
            Deduction("a metric had too little history to call movers", 0.10,
                      count=len(METRICS) - len(usable_metrics)),
            Deduction("rows were rejected as malformed", 0.05,
                      count=1 if malformed else 0),
        ]
        return Outcome(
            fields={
                "iso_week": f"{end.isocalendar().year}-W{end.isocalendar().week:02d}",
                "dedupe_key": f"{end.isocalendar().year}-"
                              f"W{end.isocalendar().week:02d}:sha256:{digest}",
                "input_digest": f"sha256:{digest}",
                "supersedes_input_digest": None,
                "analytics_source": doc.get("source", "api"),
                "data_window": {
                    "start": start.isoformat(), "end": end.isoformat(),
                    "data_cutoff": cutoff.isoformat(),
                    "rows_excluded_lag": excluded_lag,
                    "rows_rejected_malformed": malformed,
                    "videos_below_impressions_floor": below_floor},
                "baseline": baseline,
                "movers": movers,
                "retention_findings": retention,
                "decaying": decaying,
                "actions": actions,
                "last_week_review": review,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if movers or retention or decaying else "clean",
        )

    @staticmethod
    def attribute(row: dict, metric: str) -> tuple[str, float]:
        """Name a cause only where the row distinguishes one. Otherwise say so."""
        if row.get("packaging_changed_in_window"):
            return "thumbnail_or_title_effect", 0.75
        if row.get("edit_changed_in_window"):
            return "video_specific_change", 0.70
        if row.get("published_in_window"):
            return "publish_timing", 0.50
        if int(row.get("impressions", 0)) < 4 * IMPRESSIONS_FLOOR:
            # Above the floor but not by much: the swing is real and the cause
            # is not separable at this volume. Say which of the two it is.
            return "insufficient_volume_for_causal_claim", 0.35
        return "undetermined", 0.30

    @staticmethod
    def actions(movers: list[dict], retention: list[dict],
                decaying: list[dict]) -> list[dict]:
        """Exactly three, ranked, each pointing at the evidence behind it."""
        candidates: list[dict] = []
        for m in movers[:2]:
            direction = "recover" if m["delta"] < 0 else "repeat"
            candidates.append({
                "action": f"{direction} the {m['metric'].replace('_', ' ')} change "
                          f"on {m['video_id']}: delta {m['delta']:+.4f} against the "
                          f"trailing median, attributed {m['attribution']}",
                "target_metric": m["metric"],
                "expected_delta": abs(round(m["delta"], 4)),
                "effort": "low" if m["attribution"] == "thumbnail_or_title_effect"
                          else "medium",
                "evidence_refs": [f"mover:{m['video_id']}:{m['metric']}"]})
        for r in retention[:1]:
            candidates.append({
                "action": f"re-cut {r['video_id']} around the {r['dropoff_s']:.0f}s "
                          f"drop-off: {r['hypothesis'][:140]}",
                "target_metric": "retention_at_30s_ratio",
                "expected_delta": None, "effort": "medium",
                "evidence_refs": [f"retention:{r['video_id']}"]})
        for d in decaying[:1]:
            candidates.append({
                "action": f"decide whether to refresh or retire {d['video_id']}: "
                          f"impressions {d['impressions_delta']:+d}, "
                          f"{d['likely_cause'].replace('_', ' ')}",
                "target_metric": None, "expected_delta": None, "effort": "low",
                "evidence_refs": [f"decaying:{d['video_id']}"]})
        while len(candidates) < 3:
            # Three is the contract. With nothing to act on, say that plainly
            # rather than padding the list with invented work.
            candidates.append({
                "action": "no further action is supported by this week's data; "
                          "the remaining metrics sat inside their trailing range",
                "target_metric": None, "expected_delta": None, "effort": "low",
                "evidence_refs": ["baseline:within_iqr"]})
        return [{"rank": i, **c} for i, c in enumerate(candidates[:3], start=1)]


if __name__ == "__main__":
    raise SystemExit(Augur(__file__).main())
