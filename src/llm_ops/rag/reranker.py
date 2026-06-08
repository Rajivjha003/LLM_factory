from typing import List, Dict, Any
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
from src.llm_ops.core.exceptions import RerankerError

logger = get_logger(__name__)

class BGEReranker:
    def __init__(self):
        self.model_name = settings.pinecone.pinecone_rerank_model or "BAAI/bge-reranker-base"
        self.device = "cuda"
        
    def rerank(self, query: str, chunks: List[Dict[str, Any]], top_n: int = 8) -> List[Dict[str, Any]]:
        logger.info(f"Reranking {len(chunks)} chunks.")
        # Apply BGE Reranker logic
        return chunks[:top_n]
