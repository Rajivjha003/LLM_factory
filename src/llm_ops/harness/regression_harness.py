from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class RegressionHarness:
    def __init__(self):
        pass
        
    def run_eval(self):
        logger.info("Running Regression Harness against past failures.")
        if not settings.harness.run_regression_before_promotion:
            logger.warning("Regression runs before promotion are disabled.")
        # Replay past failures
        pass
