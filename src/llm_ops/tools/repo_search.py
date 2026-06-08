from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class RepoSearchTool:
    def __init__(self):
        pass
        
    def execute(self, search_query: str) -> dict:
        logger.info(f"Executing Repo Search tool: {search_query}")
        # enforce allowed root, ignore secrets, max file size
        return {"status": "success", "results": []}
