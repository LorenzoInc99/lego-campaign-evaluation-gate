from __future__ import annotations

import json
import sqlite3
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "runs.sqlite"
REPORT_PATH = ROOT / "reports" / "phase4_observability_report.md"


def _trend_label(first: float, last: float, stable_band: float = 0.15) -> str:
    delta = last - first
    if abs(delta) <= stable_band:
        return "stable"
    return "improving" if delta > 0 else "degrading"


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    rows = list(
        conn.execute(
            """
            SELECT o.run_id, r.run_type,
                   AVG(s.relevance_score) AS relevance_score,
                   AVG(s.actionability_score) AS actionability_score,
                   AVG(s.constraint_score) AS constraint_score,
                   AVG(s.structure_score) AS structure_score,
                   AVG(s.aggregate_score) AS aggregate_score
            FROM outputs o
            JOIN scores s ON s.output_id = o.output_id
            JOIN runs r ON r.run_id = o.run_id
            GROUP BY o.run_id, r.run_type
            ORDER BY o.run_id ASC
            """
        )
    )

    if not rows:
        raise RuntimeError("No run data found in runs.sqlite")

    metric_keys = [
        "relevance_score",
        "actionability_score",
        "constraint_score",
        "structure_score",
        "aggregate_score",
    ]
    trends = {}
    for key in metric_keys:
        first = float(rows[0][key])
        last = float(rows[-1][key])
        trends[key] = {"first": round(first, 3), "last": round(last, 3), "trend": _trend_label(first, last)}

    gate_rows = list(
        conn.execute(
            """
            SELECT decision_id, baseline_run_id, candidate_run_id, decision, failed_checks_json, decision_note
            FROM gate_decisions
            ORDER BY decision_id ASC
            """
        )
    )

    decision_counts = Counter(r["decision"] for r in gate_rows)
    failed_counter: Counter[str] = Counter()
    for r in gate_rows:
        try:
            payload = json.loads(r["failed_checks_json"])
            failed = payload.get("failed_checks", [])
            for item in failed:
                failed_counter[item.split("=")[0]] += 1
        except json.JSONDecodeError:
            continue

    top_failed = failed_counter.most_common(5)

    lines = []
    lines.append("# Phase 4 Observability and Governance Report")
    lines.append("")
    lines.append("## Run Trend Overview")
    lines.append("| run_id | run_type | relevance | actionability | constraints | structure | aggregate |")
    lines.append("|---:|---|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r['run_id']} | {r['run_type']} | {float(r['relevance_score']):.3f} | "
            f"{float(r['actionability_score']):.3f} | {float(r['constraint_score']):.3f} | "
            f"{float(r['structure_score']):.3f} | {float(r['aggregate_score']):.3f} |"
        )

    lines.append("")
    lines.append("## Drift Diagnostics")
    for key, info in trends.items():
        lines.append(f"- `{key}`: {info['first']:.3f} -> {info['last']:.3f} ({info['trend']})")

    lines.append("")
    lines.append("## Governance Decision Summary")
    lines.append(f"- Total decisions logged: {len(gate_rows)}")
    lines.append(f"- PROMOTE count: {decision_counts.get('PROMOTE', 0)}")
    lines.append(f"- PROMOTE_CONDITIONAL count: {decision_counts.get('PROMOTE_CONDITIONAL', 0)}")
    lines.append(f"- BLOCK count: {decision_counts.get('BLOCK', 0)}")
    lines.append("")
    lines.append("### Top Failed Check Categories")
    if top_failed:
        for key, count in top_failed:
            lines.append(f"- `{key}` occurred {count} time(s)")
    else:
        lines.append("- No failed checks recorded.")

    lines.append("")
    lines.append("## Decision Audit Trail")
    lines.append("| decision_id | baseline_run_id | candidate_run_id | decision | note |")
    lines.append("|---:|---:|---:|---|---|")
    for r in gate_rows:
        note = str(r["decision_note"]).replace("|", "/")
        lines.append(f"| {r['decision_id']} | {r['baseline_run_id']} | {r['candidate_run_id']} | {r['decision']} | {note} |")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Phase 4 report generated at {REPORT_PATH}")


if __name__ == "__main__":
    main()
