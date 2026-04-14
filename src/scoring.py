from __future__ import annotations

import json
import re
import statistics
from typing import Dict, List

from .config import AppConfig
from .llm_client import generate_text


def _extract_json(text: str) -> Dict[str, float]:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return {}
    try:
        parsed = json.loads(match.group(0))
        return {k: float(v) for k, v in parsed.items() if isinstance(v, (int, float))}
    except (ValueError, TypeError):
        return {}


def deterministic_structure_score(output_text: str) -> float:
    required_tokens = ["Action 1", "Action 2", "Action 3", "Rationale", "Target Segment", "Expected Impact"]
    found = sum(1 for token in required_tokens if token.lower() in output_text.lower())
    return round((found / len(required_tokens)) * 10.0, 2)


def deterministic_constraint_score(output_text: str, constraints: Dict[str, object]) -> float:
    checks: List[bool] = []
    budget = str(constraints.get("budget_band", "")).lower()
    channels = [str(c).lower() for c in constraints.get("channels", [])]
    segments = [str(s).lower() for s in constraints.get("segments", [])]

    text = output_text.lower()
    if budget:
        checks.append(any(tok in text for tok in budget.split()))
    if channels:
        checks.append(any(c in text for c in channels))
    if segments:
        checks.append(any(s in text for s in segments))

    if not checks:
        return 5.0
    return round((sum(1 for ok in checks if ok) / len(checks)) * 10.0, 2)


def rubric_scores_with_judge(config: AppConfig, brief_text: str, output_text: str) -> Dict[str, float]:
    judge_prompt = f"""
You are an evaluator for commercial campaign suggestions.
Score from 0 to 10. Return ONLY JSON with keys:
relevance_score, actionability_score.

Brief:
{brief_text}

Output:
{output_text}

Rubric:
- relevance_score: alignment to brief objectives, constraints, and audience.
- actionability_score: concrete next steps, decision clarity, low ambiguity.
"""
    res = generate_text(config.api_key, config.judge_model, judge_prompt, response_mime_type="application/json")
    parsed = _extract_json(str(res["text"]))
    if "relevance_score" not in parsed or "actionability_score" not in parsed:
        brief_tokens = {t for t in re.findall(r"[a-zA-Z0-9]+", brief_text.lower()) if len(t) > 3}
        output_tokens = set(re.findall(r"[a-zA-Z0-9]+", output_text.lower()))
        overlap = len(brief_tokens.intersection(output_tokens))
        denom = max(1, min(20, len(brief_tokens)))
        relevance = min(10.0, max(0.0, (overlap / denom) * 10.0))

        action_markers = ["action", "next", "launch", "test", "measure", "optimize", "segment", "budget"]
        marker_hits = sum(1 for m in action_markers if m in output_text.lower())
        actionability = min(10.0, 2.5 + marker_hits * 0.9)
        return {
            "relevance_score": round(relevance, 2),
            "actionability_score": round(actionability, 2),
        }
    return {
        "relevance_score": float(parsed.get("relevance_score", 5.0)),
        "actionability_score": float(parsed.get("actionability_score", 5.0)),
    }


def score_output(config: AppConfig, brief_text: str, constraints: Dict[str, object], output_text: str) -> Dict[str, float]:
    judge = rubric_scores_with_judge(config, brief_text, output_text)
    structure = deterministic_structure_score(output_text)
    constraint = deterministic_constraint_score(output_text, constraints)

    scores = {
        "relevance_score": round(max(0.0, min(10.0, judge["relevance_score"])), 2),
        "actionability_score": round(max(0.0, min(10.0, judge["actionability_score"])), 2),
        "constraint_score": round(max(0.0, min(10.0, constraint)), 2),
        "structure_score": round(max(0.0, min(10.0, structure)), 2),
    }
    agg = 0.0
    for metric, weight in config.scoring_weights.items():
        agg += scores[metric] * weight
    scores["aggregate_score"] = round(agg, 3)
    scores["score_variance"] = round(statistics.pvariance(scores.values()), 4)
    return scores
