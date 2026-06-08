from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def build_eval_samples(failures: list, output_dataset_path: str):
    logger.info(f"Building eval samples from failures into {output_dataset_path}")
    # Convert failure records into harness eval samples
    pass
