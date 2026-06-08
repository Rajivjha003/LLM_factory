import argparse
from src.llm_ops.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="data/rag_corpus")
    args = parser.parse_args()
    
    logger.info(f"Ingesting docs from {args.source}")
    # Call chunking and Qdrant ingestion
    
if __name__ == "__main__":
    main()
