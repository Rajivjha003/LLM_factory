from src.llm_ops.core.config import settings

def test_config_loads():
    assert settings.app.app_name == "merchmix_llm_ops"
    
def test_critical_settings_disabled():
    # Verify core security defaults are actually false
    assert settings.agent.agents_enabled is False
    assert settings.mcp.mcp_enabled is False
    assert settings.security.allow_destructive_sql is False
    assert settings.security.allow_shell_tools is False
    assert settings.security.allow_prod_write is False
    assert settings.learning_loop.auto_training_enabled is False
    assert settings.learning_loop.auto_promotion_enabled is False
    
    # Verify required ops are enabled
    assert settings.guardrail.guardrails_enabled is True
    assert settings.learning_loop.learning_loop_enabled is True
