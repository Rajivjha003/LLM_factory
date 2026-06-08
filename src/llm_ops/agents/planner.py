from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class Planner:
    def __init__(self):
        pass
        
    def create_plan(self, task: str):
        logger.info(f"Creating plan for task: {task}")
        pass
