from src.llm_ops.harness.rag_harness import RAGHarness
from src.llm_ops.core.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    harness = RAGHarness()
    harness.run_eval()
