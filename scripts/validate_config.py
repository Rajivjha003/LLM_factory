import sys
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

def main():
    try:
        # Check security critical settings
        critical_errors = []
        
        if settings.agent.agents_enabled:
            critical_errors.append("AGENTS_ENABLED must be False")
            
        if settings.mcp.mcp_enabled:
            critical_errors.append("MCP_ENABLED must be False")
            
        if settings.security.allow_destructive_sql:
            critical_errors.append("ALLOW_DESTRUCTIVE_SQL must be False")
            
        if settings.security.allow_shell_tools:
            critical_errors.append("ALLOW_SHELL_TOOLS must be False")
            
        if settings.security.allow_prod_write:
            critical_errors.append("ALLOW_PROD_WRITE must be False")
            
        if settings.learning_loop.auto_training_enabled:
            critical_errors.append("AUTO_TRAINING_ENABLED must be False")
            
        if settings.learning_loop.auto_promotion_enabled:
            critical_errors.append("AUTO_PROMOTION_ENABLED must be False")
            
        if not settings.guardrail.guardrails_enabled:
            critical_errors.append("GUARDRAILS_ENABLED must be True")
            
        if not settings.learning_loop.learning_loop_enabled:
            critical_errors.append("LEARNING_LOOP_ENABLED must be True")
            
        if critical_errors:
            logger.error("Security critical config validation failed:")
            for err in critical_errors:
                logger.error(f"- {err}")
            sys.exit(1)
            
        logger.info("Security critical config validation passed.")
        logger.info("All dangerous systems are strictly disabled.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Config validation script crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
