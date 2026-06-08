from src.llm_ops.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

def main():
    logger.info("Testing retrieval smoke")
    # Query Qdrant
    
if __name__ == "__main__":
    main()
