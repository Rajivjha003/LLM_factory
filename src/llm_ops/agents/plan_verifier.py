from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class PlanVerifier:
    def verify(self, plan: dict) -> bool:
        logger.info("Verifying plan")
        return True
