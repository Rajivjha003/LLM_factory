class LLMOpsError(Exception):
    """Base exception class for all LLM Ops errors."""
    pass

class ConfigurationError(LLMOpsError):
    """Raised when there is a configuration error."""
    pass

class CUDAError(LLMOpsError):
    """Raised when there is a CUDA-related error (OOM, not found, etc.)."""
    pass

class VRAMLimitExceededError(CUDAError):
    """Raised when an operation would exceed the configured VRAM limits."""
    pass

class ModelLoadError(LLMOpsError):
    """Raised when a model fails to load or download."""
    pass
