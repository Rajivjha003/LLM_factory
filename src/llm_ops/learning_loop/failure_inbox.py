import jsonlines
from typing import Dict, Any
from src.llm_ops.core.schemas import FailureRecord
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def log_failure(record: FailureRecord):
    if not settings.learning_loop.learning_loop_enabled:
        return
        
    path = settings.learning_loop.failure_inbox_path
    try:
        with jsonlines.open(path, mode='a') as writer:
            writer.write(record.model_dump())
        logger.info(f"Failure record saved to {path}")
    except Exception as e:
        logger.error(f"Failed to write failure record: {e}")
