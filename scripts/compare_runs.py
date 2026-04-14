from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import load_config, to_json
from src.db import (
    aggregate_scores,
    connect,
    get_latest_run_id,
    get_run_scores,
    insert_business_proxies,
    insert_gate_decision,
)
from src.gate import evaluate_gate, failed_checks_json


def main() -> None:
    config = load_config()
    conn = connect(config.db_path)
    baseline_run_id = get_latest_run_id(conn, "baseline")
    candidate_run_id = get_latest_run_id(conn, "candidate")

    baseline_rows = get_run_scores(conn, baseline_run_id)
    candidate_rows = get_run_scores(conn, candidate_run_id)
    baseline = aggregate_scores(baseline_rows)
    candidate = aggregate_scores(candidate_rows)

    sample_size = len(candidate_rows)
    result = evaluate_gate(baseline, candidate, config.thresholds, sample_size=sample_size)
    insert_gate_decision(
        conn=conn,
        baseline_run_id=baseline_run_id,
        candidate_run_id=candidate_run_id,
        decision=result.decision,
        failed_checks_json=failed_checks_json(result),
        decision_note=result.note,
    )

    # Lightweight synthetic business proxies tied to quality signal for MVP demo
    baseline_acceptance = min(0.98, max(0.50, baseline["aggregate_score"] / 10.0))
    candidate_acceptance = min(0.98, max(0.50, candidate["aggregate_score"] / 10.0))
    insert_business_proxies(conn, baseline_run_id, baseline_acceptance, 1 - baseline_acceptance, 0.18)
    insert_business_proxies(conn, candidate_run_id, candidate_acceptance, 1 - candidate_acceptance, 0.24)

    print(
        to_json(
            {
                "baseline_run_id": baseline_run_id,
                "candidate_run_id": candidate_run_id,
                "decision": result.decision,
                "failed_checks": result.failed_checks,
                "deltas": result.deltas,
                "warnings": result.warnings,
                "sample_size": result.sample_size,
                "variance_gate_applied": result.variance_gate_applied,
                "confidence": result.confidence,
            }
        )
    )


if __name__ == "__main__":
    main()
