class LLMOpsError(Exception):
    """Base exception for all llm_ops errors."""
    pass

class ConfigError(LLMOpsError):
    pass

class ModelLoadError(LLMOpsError):
    pass

class RetrievalError(LLMOpsError):
    pass

class RerankerError(LLMOpsError):
    pass

class RAGAnswerError(LLMOpsError):
    pass

class GuardrailViolation(LLMOpsError):
    pass

class SelfEvalFailure(LLMOpsError):
    pass

class ToolExecutionError(LLMOpsError):
    pass

class UnsafeSQLError(LLMOpsError):
    pass

class AgentExecutionError(LLMOpsError):
    pass

class ObservabilityError(LLMOpsError):
    pass
