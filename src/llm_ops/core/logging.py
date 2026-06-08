import sys
import uuid
from loguru import logger
from contextvars import ContextVar
from typing import Optional
from .config import settings

request_id_ctx_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)
trace_id_ctx_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)

def _get_context_filter(record):
    req_id = request_id_ctx_var.get()
    record["extra"]["request_id"] = req_id if req_id else "NO_REQ_ID"
    
    trace_id = trace_id_ctx_var.get()
    record["extra"]["trace_id"] = trace_id if trace_id else "NO_TRACE_ID"
    
    return True

def setup_logging():
    logger.remove()
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "req:<magenta>{extra[request_id]}</magenta> trace:<blue>{extra[trace_id]}</blue> - "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.app.app_log_level,
        filter=_get_context_filter
    )
    
    if settings.app.app_env != "local":
        logger.add(
            "logs/app.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | req:{extra[request_id]} trace:{extra[trace_id]} - {message}",
            serialize=True,
            level="INFO",
            filter=_get_context_filter,
            rotation="10 MB",
            retention="10 days"
        )

def get_logger(name: str = None):
    if name:
        return logger.bind(module=name)
    return logger
