import torch
from sentence_transformers import CrossEncoder
from typing import List, Dict, Any
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

class Reranker:
    def __init__(self):
        self.model = None
        self.device = None
        
    def load_model(self):
        if self.model is not None:
            return
            
        if not settings.reranker.reranker_enabled:
            return
            
        target_device = settings.reranker.reranker_device
        if target_device == "cuda" and not torch.cuda.is_available():
            if settings.reranker.reranker_allow_cpu_fallback:
                logger.warning("CUDA requested but not available. Falling back to CPU for reranker.")
                target_device = "cpu"
            else:
                logger.error("CUDA is not available and CPU fallback is disabled for reranker.")
                raise RuntimeError("CUDA not available for reranker.")
                
        self.device = target_device
        logger.info(f"Loading reranker model: {settings.reranker.reranker_model} on {self.device}")
        try:
            self.model = CrossEncoder(settings.reranker.reranker_model, device=self.device)
        except Exception as e:
            logger.error(f"Failed to load reranker model: {e}")
            raise e

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_n: int = None) -> List[Dict[str, Any]]:
        if not settings.reranker.reranker_enabled:
            return candidates
            
        if not candidates:
            return []
            
        if not query.strip():
            logger.warning("Empty query passed to reranker.")
            return candidates
            
        self.load_model()
        if top_n is None:
            top_n = settings.reranker.reranker_top_n
            
        pairs = []
        for c in candidates:
            text = c["payload"].get("text", "")
            if not text.strip():
                text = " "
            pairs.append([query, text])
            
        scores = self.model.predict(
            pairs, 
            batch_size=settings.reranker.reranker_batch_size, 
            show_progress_bar=False
        )
        
        # Attach scores
        for i, c in enumerate(candidates):
            c["rerank_score"] = float(scores[i])
            
        # Sort and slice
        reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:top_n]
        
        # Replace main score so downstream sees highest rank
        for r in reranked:
            r["score"] = r["rerank_score"]
            
        return reranked

reranker_layer = Reranker()
