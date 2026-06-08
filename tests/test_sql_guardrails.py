from src.llm_ops.guardrails.sql_guardrails import check_sql_safety

def test_unsafe_sql_blocked():
    bad_sql = [
        "DROP TABLE users;",
        "DELETE FROM merchmix.sales WHERE date < '2023-01-01'",
        "TRUNCATE TABLE logs;",
        "ALTER TABLE styles ADD COLUMN new_col STRING",
        "INSERT INTO test VALUES (1)"
    ]
    
    for sql in bad_sql:
        res = check_sql_safety(sql)
        assert res.passed is False
        
def test_safe_sql_passes():
    good_sql = [
        "SELECT * FROM users LIMIT 10;",
        "WITH cte AS (SELECT 1) SELECT * FROM cte;",
        "EXPLAIN SELECT id FROM logs;"
    ]
    
    for sql in good_sql:
        res = check_sql_safety(sql)
        assert res.passed is True
