# Evaluation report

## Run Overview
- Baseline run id: `21`
- Candidate run id: `22`
- Gate decision: **BLOCK**
- Decision note: Candidate blocked by reliability gate.
- Sample size: `8` case(s)
- Variance gate applied: `True`
- Confidence: `1.00` (high sample support)

## Pairwise Release Summary
- Δ Relevance: `-0.065`
- Δ Actionability: `-0.450`
- Δ Constraints: `-0.416`
- Δ Structure: `-0.210`
- Δ Aggregate: `-0.302`
- Decision: **BLOCK**
- Confidence: `1.00`

## Scorecard
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| relevance_score | 2.966 | 2.901 | -0.065 |
| actionability_score | 4.750 | 4.300 | -0.450 |
| constraint_score | 7.501 | 7.085 | -0.416 |
| structure_score | 4.165 | 3.955 | -0.210 |
| aggregate_score | 4.844 | 4.542 | -0.302 |
| score_variance | 3.459 | 4.297 | +0.839 |

## Gate Checks
- aggregate_drop_pct=6.23% > 5.00%
- actionability_drop_pct=9.47% > 8.00%
- variance_delta_abs=0.839 > 0.500

## Data Sufficiency Notes
- No warnings.

## Business Proxy Panel
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| acceptance_rate | 0.500 | 0.500 | +0.000 |
| rewrite_rate | 0.500 | 0.500 | +0.000 |
| clarification_rate | 0.180 | 0.240 | +0.060 |

## Failure Scenario
Candidate prompt changes can look stronger on readability while still regressing on operational quality.
This report separates hard quality failures from stability checks and applies sample-size-aware logic.
