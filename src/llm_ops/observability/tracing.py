import uuid
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def generate_trace_id() -> str:
    return str(uuid.uuid4())

def setup_opentelemetry():
    if not settings.langfuse.langfuse_enabled:
        return
        
    logger.info("Setting up OpenTelemetry exporter.")
    # Setup OTLP exporter
    pass
