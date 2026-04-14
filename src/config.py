from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"


def _load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and key not in os.environ:
            os.environ[key] = value


_load_env()


@dataclass(frozen=True)
class ModelConfig:
    name: str
    temperature: float
    max_output_tokens: int


@dataclass(frozen=True)
class GateThresholds:
    aggregate_drop_pct: float = 5.0
    actionability_drop_pct: float = 8.0
    variance_delta_abs: float = 0.5
    min_cases_for_variance_gate: int = 5
    min_constraint_score: float = 3.0
    min_structure_score: float = 3.0


@dataclass(frozen=True)
class AppConfig:
    api_key: str
    baseline_prompt_version: str
    candidate_prompt_version: str
    model: ModelConfig
    judge_model: ModelConfig
    scoring_weights: Dict[str, float]
    thresholds: GateThresholds
    db_path: Path
    dataset_path: Path
    report_path: Path
    evaluator_version: str = "v1.0"


def load_config() -> AppConfig:
    api_key = os.environ.get("Gemini_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing Gemini_API_KEY in environment/.env")

    db_path = DATA_DIR / "runs.sqlite"
    dataset_override = os.environ.get("DATASET_PATH", "").strip()
    dataset_path = Path(dataset_override) if dataset_override else (DATA_DIR / "test_cases.jsonl")
    report_path = REPORTS_DIR / "latest_report.md"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    baseline_prompt_version = os.environ.get("BASELINE_PROMPT_VERSION", "v1-baseline").strip() or "v1-baseline"
    candidate_prompt_version = os.environ.get("CANDIDATE_PROMPT_VERSION", "v2-verbose").strip() or "v2-verbose"
    model_temperature = float(os.environ.get("MODEL_TEMPERATURE", "0.2"))
    judge_temperature = float(os.environ.get("JUDGE_TEMPERATURE", "0.0"))

    return AppConfig(
        api_key=api_key,
        baseline_prompt_version=baseline_prompt_version,
        candidate_prompt_version=candidate_prompt_version,
        model=ModelConfig(name="gemini-2.5-flash", temperature=model_temperature, max_output_tokens=1200),
        judge_model=ModelConfig(name="gemini-2.5-flash", temperature=judge_temperature, max_output_tokens=400),
        scoring_weights={
            "relevance_score": 0.30,
            "actionability_score": 0.35,
            "constraint_score": 0.25,
            "structure_score": 0.10,
        },
        thresholds=GateThresholds(),
        db_path=db_path,
        dataset_path=dataset_path,
        report_path=report_path,
    )


def to_json(data: Dict[str, object]) -> str:
    return json.dumps(data, ensure_ascii=True, sort_keys=True)
