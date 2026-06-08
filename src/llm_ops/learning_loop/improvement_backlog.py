from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def add_to_backlog(item: dict, backlog_path: str):
    logger.info(f"Adding improvement item to backlog: {backlog_path}")
    # Track RAG corpus fixes, prompt fixes, tool fixes needed
    pass
