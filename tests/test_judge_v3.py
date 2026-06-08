import pytest
from llm_ops.eval.judge_v3 import judge_response_v3
from types import SimpleNamespace

def test_judge_v3_passes_when_sql_good_but_v2_strict():
    # If a sample requires "specific_term" but the response doesn't have it, v2 fails.
    # But if the SQL is perfect, v3 should pass it and flag human_review_required.
    sample = SimpleNamespace(
        id="test_001",
        domain="sql_generation",
        prompt="Write a query to get duplicate users.",
        must_include=["specific_term"],
        must_not_include=[],
        expected_traits=["check for duplicates"]
    )
    response = "Here is the query:\n```sql\nSELECT user, COUNT(*) FROM t GROUP BY user HAVING COUNT(*) > 1;\n```"
    result = judge_response_v3(sample, response)
    
    assert not result.passed_v2 # Failed strict regression gate (missing 'specific_term')
    assert result.passed_v3 # Passed semantic SQL gate
    assert result.human_review_required # Flagged for human review

def test_judge_v3_fails_when_sql_unsafe():
    sample = SimpleNamespace(
        id="test_002",
        domain="sql_generation",
        prompt="Give me all users.",
        must_include=[],
        must_not_include=[],
        expected_traits=[]
    )
    response = "```sql\nDROP TABLE users;\n```"
    result = judge_response_v3(sample, response)
    
    assert not result.passed_v3
    assert not result.passed_v2
