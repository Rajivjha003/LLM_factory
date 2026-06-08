import sys
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

def main():
    try:
        # Just accessing properties to ensure they load
        app_name = settings.app.app_name
        logger.info(f"Config loaded successfully for app: {app_name}")
        logger.info(f"Guardrails enabled: {settings.guardrail.guardrails_enabled}")
        logger.info(f"Agents enabled: {settings.agent.agents_enabled}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Config validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
