from src.llm_ops.core.config import settings

def test_config_loads():
    assert settings.app.app_name == "merchmix_llm_ops"
    assert settings.guardrail.guardrails_enabled is True
    print("Config loaded successfully")
    
if __name__ == "__main__":
    test_config_loads()
