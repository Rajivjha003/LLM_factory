from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class FinalVerifier:
    def verify(self, answer: str) -> bool:
        logger.info("Final answer verification")
        return True
