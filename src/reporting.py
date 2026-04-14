from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def _row(metric: str, baseline: float, candidate: float) -> str:
    delta = candidate - baseline
    return f"| {metric} | {baseline:.3f} | {candidate:.3f} | {delta:+.3f} |"


def build_report(
    baseline_run_id: int,
    candidate_run_id: int,
    baseline: Dict[str, float],
    candidate: Dict[str, float],
    gate_decision: str,
    failed_checks: List[str],
    gate_note: str,
    gate_warnings: List[str],
    sample_size: int,
    variance_gate_applied: bool,
    confidence: float,
    business_baseline: Dict[str, float] | None,
    business_candidate: Dict[str, float] | None,
) -> str:
    checks = "\n".join(f"- {c}" for c in failed_checks) if failed_checks else "- No failed checks."
    warnings = "\n".join(f"- {w}" for w in gate_warnings) if gate_warnings else "- No warnings."
    business_lines = []
    if business_baseline and business_candidate:
        business_lines.append("| Metric | Baseline | Candidate | Delta |")
        business_lines.append("|---|---:|---:|---:|")
        for key in ("acceptance_rate", "rewrite_rate", "clarification_rate"):
            b = float(business_baseline.get(key, 0.0))
            c = float(business_candidate.get(key, 0.0))
            business_lines.append(f"| {key} | {b:.3f} | {c:.3f} | {c-b:+.3f} |")
    else:
        business_lines.append("- Business proxy data not available.")

    return f"""# Phase 3 Evaluation Report

## Run Overview
- Baseline run id: `{baseline_run_id}`
- Candidate run id: `{candidate_run_id}`
- Gate decision: **{gate_decision}**
- Decision note: {gate_note}
- Sample size: `{sample_size}` case(s)
- Variance gate applied: `{variance_gate_applied}`
- Confidence: `{confidence:.2f}` ({'high' if confidence >= 0.8 else 'medium' if confidence >= 0.5 else 'low'} sample support)

## Pairwise Release Summary
- Δ Relevance: `{candidate["relevance_score"] - baseline["relevance_score"]:+.3f}`
- Δ Actionability: `{candidate["actionability_score"] - baseline["actionability_score"]:+.3f}`
- Δ Constraints: `{candidate["constraint_score"] - baseline["constraint_score"]:+.3f}`
- Δ Structure: `{candidate["structure_score"] - baseline["structure_score"]:+.3f}`
- Δ Aggregate: `{candidate["aggregate_score"] - baseline["aggregate_score"]:+.3f}`
- Decision: **{gate_decision}**
- Confidence: `{confidence:.2f}`

## Scorecard
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
{_row("relevance_score", baseline["relevance_score"], candidate["relevance_score"])}
{_row("actionability_score", baseline["actionability_score"], candidate["actionability_score"])}
{_row("constraint_score", baseline["constraint_score"], candidate["constraint_score"])}
{_row("structure_score", baseline["structure_score"], candidate["structure_score"])}
{_row("aggregate_score", baseline["aggregate_score"], candidate["aggregate_score"])}
{_row("score_variance", baseline["score_variance"], candidate["score_variance"])}

## Gate Checks
{checks}

## Data Sufficiency Notes
{warnings}

## Business Proxy Panel
{chr(10).join(business_lines)}

## Failure Scenario
Candidate prompt changes can look stronger on readability while still regressing on operational quality.
This report separates hard quality failures from stability checks and applies sample-size-aware logic.
"""


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
