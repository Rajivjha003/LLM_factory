from src.llm_ops.harness.production_replay_harness import ProductionReplayHarness
from src.llm_ops.core.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    harness = ProductionReplayHarness()
    harness.run_eval()
