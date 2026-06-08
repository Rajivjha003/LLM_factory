from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class SupervisorAgent:
    def __init__(self):
        self.enabled = settings.agent.agents_enabled
        if not self.enabled:
            logger.warning("SupervisorAgent initialized but AGENTS_ENABLED=false")
            
    def run(self, task: str):
        logger.info(f"SupervisorAgent running task: {task}")
        pass
