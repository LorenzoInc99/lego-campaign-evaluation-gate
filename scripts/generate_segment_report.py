#!/usr/bin/env python3
"""Build segmented evaluation report from validation_suite + SQLite scores."""

from __future__ import annotations

import json
import os
import sqlite3
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "runs.sqlite"
SUITE_PATH = ROOT / "data" / "validation_suite.jsonl"
REPORT_PATH = ROOT / "reports" / "segment_report.md"


def load_suite() -> list[dict]:
    rows = []
    for line in SUITE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def fetch_scores(conn: sqlite3.Connection, run_id: int) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    cur = conn.execute(
        """
        SELECT o.test_case_id, s.relevance_score, s.actionability_score, s.constraint_score,
               s.structure_score, s.aggregate_score
        FROM outputs o
        JOIN scores s ON s.output_id = o.output_id
        WHERE o.run_id = ?
        """,
        (run_id,),
    )
    for row in cur.fetchall():
        tc = str(row[0])
        out[tc] = {
            "relevance_score": float(row[1]),
            "actionability_score": float(row[2]),
            "constraint_score": float(row[3]),
            "structure_score": float(row[4]),
            "aggregate_score": float(row[5]),
        }
    return out


def mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else 0.0


def suite_signal(mean_delta: float, n: int) -> str:
    if n == 0:
        return "N/A"
    if mean_delta > 0.05:
        return "PROMOTE_SEGMENT"
    if mean_delta < -0.05:
        return "BLOCK_SEGMENT"
    return "FLAT"


def main() -> None:
    baseline_run = int(os.environ.get("SEGMENT_BASELINE_RUN", "21"))
    candidate_run = int(os.environ.get("SEGMENT_CANDIDATE_RUN", "22"))

    suite_rows = load_suite()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    base = fetch_scores(conn, baseline_run)
    cand = fetch_scores(conn, candidate_run)

    by_segment: dict[str, list[str]] = defaultdict(list)
    for row in suite_rows:
        seg = str(row.get("evaluation_segment", "unknown"))
        by_segment[seg].append(str(row["test_case_id"]))

    lines: list[str] = []
    lines.append("# Segmented evaluation report")
    lines.append("")
    lines.append(f"- Baseline run: `{baseline_run}`")
    lines.append(f"- Candidate run: `{candidate_run}`")
    lines.append(f"- Source: `{SUITE_PATH.name}`")
    lines.append("")

    lines.append("## By `evaluation_segment` (data-backed)")
    lines.append("")
    lines.append("| Segment | Cases | n | Mean agg baseline | Mean agg candidate | Mean Δ aggregate | Signal |")
    lines.append("|---|---|---:|---:|---:|---:|---|")

    for seg in sorted(by_segment.keys()):
        tcs = by_segment[seg]
        deltas = []
        b_aggs = []
        c_aggs = []
        for tc in tcs:
            if tc not in base or tc not in cand:
                continue
            b_aggs.append(base[tc]["aggregate_score"])
            c_aggs.append(cand[tc]["aggregate_score"])
            deltas.append(cand[tc]["aggregate_score"] - base[tc]["aggregate_score"])
        n = len(deltas)
        if n == 0:
            continue
        mb = mean(b_aggs)
        mc = mean(c_aggs)
        md = mean(deltas)
        sig = suite_signal(md, n)
        lines.append(
            f"| {seg} | {', '.join(tcs)} | {n} | {mb:.3f} | {mc:.3f} | {md:+.3f} | **{sig}** |"
        )

    # Rollup groups (insight-focused)
    rollup = {
        "launch": ["TC01"],
        "multi_audience_briefs": ["TC02", "TC10", "TC12"],
        "sustainability": ["TC10"],
        "stress": ["TC11", "TC12"],
    }

    lines.append("")
    lines.append("## Rollup groups (narrative alignment)")
    lines.append("")
    lines.append("| Group | Cases | n | Mean Δ aggregate | Signal | Notes |")
    lines.append("|---|---|---:|---:|---|---|")

    notes_map = {
        "launch": "Single structured launch brief.",
        "multi_audience_briefs": "Briefs with multiple segments and/or channels.",
        "sustainability": "EU sustainability storytelling (parents + educators).",
        "stress": "Ambiguous or conflicting constraints.",
    }

    for name, tcs in rollup.items():
        deltas = []
        for tc in tcs:
            if tc not in base or tc not in cand:
                continue
            deltas.append(cand[tc]["aggregate_score"] - base[tc]["aggregate_score"])
        n = len(deltas)
        md = mean(deltas) if deltas else 0.0
        sig = suite_signal(md, n)
        lines.append(
            f"| {name} | {', '.join(tcs)} | {n} | {md:+.3f} | **{sig}** | {notes_map.get(name, '')} |"
        )

    lines.append("")
    lines.append("## How to read `Signal`")
    lines.append("")
    lines.append("- **PROMOTE_SEGMENT**: mean aggregate improved vs baseline for that slice (toy threshold ±0.05).")
    lines.append("- **BLOCK_SEGMENT**: mean aggregate worsened materially for that slice.")
    lines.append("- **FLAT**: mixed or neutral on average — treat as no global claim for that slice.")
    lines.append("")
    lines.append("Portfolio gate on the full 8 cases remains authoritative for **global** release; segments explain *where* v3 helps or hurts.")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
