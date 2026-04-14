from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import load_config
from src.db import (
    aggregate_scores,
    connect,
    get_business_proxy,
    get_latest_run_id,
    get_run_scores,
)
from src.gate import evaluate_gate
from src.reporting import build_report, write_report


def _dict_or_none(row):
    if row is None:
        return None
    return {
        "acceptance_rate": float(row["acceptance_rate"]),
        "rewrite_rate": float(row["rewrite_rate"]),
        "clarification_rate": float(row["clarification_rate"]),
    }


def main() -> None:
    config = load_config()
    conn = connect(config.db_path)
    baseline_run_id = get_latest_run_id(conn, "baseline")
    candidate_run_id = get_latest_run_id(conn, "candidate")
    baseline_rows = get_run_scores(conn, baseline_run_id)
    candidate_rows = get_run_scores(conn, candidate_run_id)
    baseline = aggregate_scores(baseline_rows)
    candidate = aggregate_scores(candidate_rows)
    gate = evaluate_gate(baseline, candidate, config.thresholds, sample_size=len(candidate_rows))

    report = build_report(
        baseline_run_id=baseline_run_id,
        candidate_run_id=candidate_run_id,
        baseline=baseline,
        candidate=candidate,
        gate_decision=gate.decision,
        failed_checks=gate.failed_checks,
        gate_note=gate.note,
        gate_warnings=gate.warnings,
        sample_size=gate.sample_size,
        variance_gate_applied=gate.variance_gate_applied,
        confidence=gate.confidence,
        business_baseline=_dict_or_none(get_business_proxy(conn, baseline_run_id)),
        business_candidate=_dict_or_none(get_business_proxy(conn, candidate_run_id)),
    )
    write_report(config.report_path, report)
    print(f"Report generated at {config.report_path}")


if __name__ == "__main__":
    main()
