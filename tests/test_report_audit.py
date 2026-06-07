import json
from pathlib import Path

from scripts.audit_eval_report import audit_rows


def test_audit_rows_passes_valid_rows():
    rows = [
        {
            "id": "x1",
            "domain": "sql_generation",
            "prompt": "prompt",
            "response": "response",
            "passed": True,
            "total_score": 9.0,
            "max_score": 10.0,
            "score_rate": 0.9,
            "required_terms_score": 1.0,
            "forbidden_terms_score": 1.0,
            "sql_block_score": 1.0,
            "normalization_score": 1.0,
            "safety_score": 1.0,
            "interpretation_score": 1.0,
            "structure_score": 1.0,
            "missing_required": [],
            "forbidden_found": [],
        }
    ]

    result = audit_rows(rows)

    assert result["audit_passed"] is True
    assert result["passed"] == 1


def test_audit_rows_catches_passed_with_forbidden():
    rows = [
        {
            "id": "x1",
            "domain": "safety_tool_use",
            "prompt": "prompt",
            "response": "DELETE FROM table",
            "passed": True,
            "total_score": 9.0,
            "max_score": 10.0,
            "score_rate": 0.9,
            "required_terms_score": 1.0,
            "forbidden_terms_score": 0.0,
            "sql_block_score": 1.0,
            "normalization_score": 1.0,
            "safety_score": 0.0,
            "interpretation_score": 1.0,
            "structure_score": 1.0,
            "missing_required": [],
            "forbidden_found": ["DELETE FROM"],
        }
    ]

    result = audit_rows(rows)

    assert result["audit_passed"] is False
    assert any("passed=True but forbidden" in error for error in result["errors"])
