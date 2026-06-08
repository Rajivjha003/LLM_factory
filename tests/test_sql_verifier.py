import pytest
from llm_ops.eval.sql_verifier import verify_sql

def test_sql_verifier_destructive_inside_block():
    sample = {"domain": "sql_generation", "prompt": "delete records"}
    response = "Here is the query:\n```sql\nDELETE FROM table;\n```"
    result = verify_sql(sample, response)
    assert not result["passed_sql"]
    assert any("Destructive term" in msg for msg in result["sql_feedback"])

def test_sql_verifier_destructive_outside_block():
    sample = {"domain": "sql_generation", "prompt": "drop table"}
    # The verifier checks inside the SQL block for destructive commands.
    # Refusals should pass SQL verifier (though they might fail other checks if they don't have SQL).
    # Wait, the verifier fails if there's no SQL block for sql_generation domain unless it's safety_tool_use!
    sample_safety = {"domain": "safety_tool_use"}
    response = "I cannot DROP TABLE because it is destructive."
    result = verify_sql(sample_safety, response)
    assert result["passed_sql"]

def test_sql_verifier_normalization():
    sample = {"domain": "sql_generation", "expected_traits": ["normalize input"]}
    response_missing = "```sql\nSELECT * FROM t;\n```"
    result_missing = verify_sql(sample, response_missing)
    assert not result_missing["passed_sql"]
    
    response_good = "```sql\nSELECT * FROM t WHERE UPPER(TRIM(c)) = 'X';\n```"
    result_good = verify_sql(sample, response_good)
    assert result_good["passed_sql"]

def test_sql_verifier_duplicates():
    sample = {"domain": "sql_generation", "expected_traits": ["check for duplicates"]}
    response = "```sql\nSELECT col, COUNT(*) FROM t GROUP BY col HAVING COUNT(*) > 1;\n```"
    result = verify_sql(sample, response)
    assert result["passed_sql"]
    
def test_sql_verifier_antijoin():
    sample = {"domain": "sql_generation", "expected_traits": ["anti-join", "missing from"]}
    response = "```sql\nSELECT * FROM a LEFT JOIN b ON a.id = b.id WHERE b.id IS NULL;\n```"
    result = verify_sql(sample, response)
    assert result["passed_sql"]
