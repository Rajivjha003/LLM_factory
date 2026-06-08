from src.llm_ops.guardrails.sql_guardrails import check_sql_safety

def test_unsafe_sql():
    res = check_sql_safety("DROP TABLE users;")
    assert res.passed == False
    print("Unsafe SQL test passed")
    
if __name__ == "__main__":
    test_unsafe_sql()
