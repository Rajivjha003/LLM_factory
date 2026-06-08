from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class LangfuseWrapper:
    def __init__(self):
        self.enabled = settings.langfuse.langfuse_enabled
        if self.enabled:
            logger.info("Langfuse tracking is ENABLED.")
            # import langfuse
            # self.client = langfuse.Langfuse(...)
        else:
            logger.info("Langfuse tracking is DISABLED. Running in no-op mode.")
            
    def trace(self, *args, **kwargs):
        if not self.enabled:
            return DummyTrace()
        # return self.client.trace(...)
        pass

class DummyTrace:
    def span(self, *args, **kwargs):
        return DummySpan()
    def update(self, *args, **kwargs):
        pass

class DummySpan:
    def generation(self, *args, **kwargs):
        return DummyGeneration()
    def update(self, *args, **kwargs):
        pass

class DummyGeneration:
    def update(self, *args, **kwargs):
        pass

langfuse_client = LangfuseWrapper()
