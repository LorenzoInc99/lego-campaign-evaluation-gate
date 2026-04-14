from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List

from .config import GateThresholds


@dataclass
class GateResult:
    decision: str
    failed_checks: List[str]
    note: str
    deltas: Dict[str, float]
    warnings: List[str]
    sample_size: int
    variance_gate_applied: bool
    confidence: float


def _pct_drop(base: float, candidate: float) -> float:
    if base == 0:
        return 0.0
    return ((base - candidate) / base) * 100.0


def evaluate_gate(
    baseline: Dict[str, float], candidate: Dict[str, float], thresholds: GateThresholds, sample_size: int
) -> GateResult:
    failed: List[str] = []
    warnings: List[str] = []
    aggregate_drop = _pct_drop(baseline["aggregate_score"], candidate["aggregate_score"])
    actionability_drop = _pct_drop(baseline["actionability_score"], candidate["actionability_score"])

    variance_delta_abs = candidate["score_variance"] - baseline["score_variance"]

    # Hard failures first: block if core viability metrics collapse.
    if candidate["constraint_score"] < thresholds.min_constraint_score:
        failed.append(f"constraint_score={candidate['constraint_score']:.2f} < {thresholds.min_constraint_score:.2f}")
    if candidate["structure_score"] < thresholds.min_structure_score:
        failed.append(f"structure_score={candidate['structure_score']:.2f} < {thresholds.min_structure_score:.2f}")

    if aggregate_drop > thresholds.aggregate_drop_pct:
        failed.append(f"aggregate_drop_pct={aggregate_drop:.2f}% > {thresholds.aggregate_drop_pct:.2f}%")
    if actionability_drop > thresholds.actionability_drop_pct:
        failed.append(f"actionability_drop_pct={actionability_drop:.2f}% > {thresholds.actionability_drop_pct:.2f}%")

    variance_gate_applied = sample_size >= thresholds.min_cases_for_variance_gate
    if variance_gate_applied:
        if variance_delta_abs > thresholds.variance_delta_abs:
            failed.append(f"variance_delta_abs={variance_delta_abs:.3f} > {thresholds.variance_delta_abs:.3f}")
    else:
        warnings.append(
            f"variance_gate_skipped: n={sample_size} < min_cases={thresholds.min_cases_for_variance_gate}"
        )

    confidence = min(1.0, sample_size / max(1, thresholds.min_cases_for_variance_gate))

    if failed:
        decision = "BLOCK"
        note = "Candidate blocked by reliability gate."
    elif warnings:
        decision = "PROMOTE_CONDITIONAL"
        note = "Candidate passes quality checks with limited sample-size confidence."
    else:
        decision = "PROMOTE"
        note = "Candidate passes reliability gate."
    return GateResult(
        decision=decision,
        failed_checks=failed,
        note=note,
        deltas={
            "aggregate_drop_pct": round(aggregate_drop, 3),
            "actionability_drop_pct": round(actionability_drop, 3),
            "variance_delta_abs": round(variance_delta_abs, 4),
        },
        warnings=warnings,
        sample_size=sample_size,
        variance_gate_applied=variance_gate_applied,
        confidence=round(confidence, 3),
    )


def failed_checks_json(result: GateResult) -> str:
    return json.dumps(
        {
            "failed_checks": result.failed_checks,
            "deltas": result.deltas,
            "warnings": result.warnings,
            "sample_size": result.sample_size,
            "variance_gate_applied": result.variance_gate_applied,
            "confidence": result.confidence,
        },
        ensure_ascii=True,
    )
