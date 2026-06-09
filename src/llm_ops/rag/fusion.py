from typing import List, Dict, Any
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger

logger = get_logger(__name__)

def reciprocal_rank_fusion(dense_results: List[Dict[str, Any]], sparse_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    k = settings.rag.rrf_k
    fused_scores = {}
    chunk_data = {}
    
    # Process dense results
    for rank, res in enumerate(dense_results):
        chunk_id = res["id"]
        if chunk_id not in fused_scores:
            fused_scores[chunk_id] = 0.0
            chunk_data[chunk_id] = res
            chunk_data[chunk_id]["dense_score"] = res["score"]
            chunk_data[chunk_id]["sparse_score"] = 0.0
            
        fused_scores[chunk_id] += 1.0 / (k + rank + 1)
        
    # Process sparse results
    for rank, res in enumerate(sparse_results):
        chunk_id = res["id"]
        if chunk_id not in fused_scores:
            fused_scores[chunk_id] = 0.0
            chunk_data[chunk_id] = res
            chunk_data[chunk_id]["dense_score"] = 0.0
            chunk_data[chunk_id]["sparse_score"] = res["score"]
            
        fused_scores[chunk_id] += 1.0 / (k + rank + 1)
        
    # Sort and map
    sorted_chunks = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    
    final_results = []
    for chunk_id, fused_score in sorted_chunks:
        data = chunk_data[chunk_id]
        data["score"] = fused_score  # Replace with RRF score
        data["rrf_score"] = fused_score
        final_results.append(data)
        
    logger.debug(f"Fused {len(dense_results)} dense and {len(sparse_results)} sparse into {len(final_results)} results using RRF.")
    return final_results
