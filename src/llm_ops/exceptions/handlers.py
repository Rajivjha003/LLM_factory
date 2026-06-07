import logging
import sys
from typing import Callable, Any
from functools import wraps

from .errors import LLMOpsError, CUDAError

logger = logging.getLogger(__name__)

def handle_exceptions(reraise: bool = True) -> Callable:
    """Decorator to catch, log, and optionally reraise exceptions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except CUDAError as e:
                logger.error(f"CUDA Error in {func.__name__}: {e}")
                if reraise:
                    raise
            except LLMOpsError as e:
                logger.error(f"LLM Ops Error in {func.__name__}: {e}")
                if reraise:
                    raise
            except Exception as e:
                logger.exception(f"Unexpected error in {func.__name__}: {e}")
                if reraise:
                    raise
        return wrapper
    return decorator

def setup_global_exception_handler():
    """Sets up a global exception handler for uncaught exceptions."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
