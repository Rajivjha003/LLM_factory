from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from llm_ops.security.subprocess_runner import (
    CommandExecutionError,
    CommandNotAllowedError,
    SafeSubprocessRunner,
)

router = APIRouter(prefix="/api/v1/data", tags=["data"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]

ALLOWED_DATA_ACTIONS = {
    "validate_eval_v2": [
        "python",
        "scripts/validate_eval_data.py",
        "--eval-dir",
        "data/eval_v2",
        "--expected-count",
        "50",
    ],
    "hash_eval_v2": [
        "python",
        "scripts/build_dataset_hash_manifest.py",
        "--dataset-dir",
        "data/eval_v2",
        "--output",
        "reports/eval_reports/eval_v2_hash_manifest.json",
    ],
    "validate_sft_v2": [
        "python",
        "scripts/validate_sft_data.py",
        "--path",
        "data/sft/merchmix_sft_v2.jsonl",
    ],
    "inspect_sft_v2": [
        "python",
        "scripts/inspect_sft_data.py",
        "--path",
        "data/sft/merchmix_sft_v2.jsonl",
    ],
    "check_overlap_v2": [
        "python",
        "scripts/check_sft_eval_overlap_strict.py",
        "--sft",
        "data/sft/merchmix_sft_v2.jsonl",
        "--eval-dir",
        "data/eval_v2",
        "--output",
        "reports/eval_reports/sft_v2_eval_v2_overlap_strict_report.md",
        "--fail-threshold",
        "0.80",
    ],
    "build_sft_v3": [
        "python",
        "scripts/build_failure_driven_sft_v3.py",
        "--base-sft",
        "data/sft/merchmix_sft_v2.jsonl",
        "--failure-report",
        "reports/failure_taxonomy/qwen_1_5b_sft_v1_eval_v2_failure_taxonomy.md",
        "--eval-jsonl",
        "reports/eval_reports/qwen_1_5b_sft_v1_eval_v2.jsonl",
        "--output",
        "data/sft/merchmix_sft_v3.jsonl",
        "--target-count",
        "500",
    ],
}

runner = SafeSubprocessRunner(
    project_root=PROJECT_ROOT,
    allowed_actions=ALLOWED_DATA_ACTIONS,
)


class DataActionRequest(BaseModel):
    action: str


@router.post("/run")
def run_data_action(request: DataActionRequest):
    try:
        result = runner.run(request.action)
        return {
            "action": result.action,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except CommandNotAllowedError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except CommandExecutionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}") from exc
