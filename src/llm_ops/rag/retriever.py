from typing import List, Dict, Any
import time
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
from src.llm_ops.rag.embeddings import embedding_layer
from src.llm_ops.rag.qdrant_store import qdrant_store
from src.llm_ops.rag.sparse_retriever import sparse_retriever
from src.llm_ops.rag.fusion import reciprocal_rank_fusion
from src.llm_ops.rag.reranker import reranker_layer

logger = get_logger(__name__)

class Retriever:
    def retrieve(self, query: str) -> Dict[str, Any]:
        start_time = time.time()
        mode = settings.rag.rag_mode
        top_k = settings.rag.rag_top_k_final
        
        dense_results = []
        sparse_results = []
        final_results = []
        
        try:
            if mode in ["dense", "hybrid", "hybrid_rerank"]:
                dense_start = time.time()
                query_vector = embedding_layer.embed_query(query)
                dense_results = qdrant_store.search_dense(
                    collection_name=settings.qdrant.qdrant_collection_docs,
                    query_vector=query_vector,
                    top_k=settings.rag.rag_top_k_dense
                )
                logger.debug(f"Dense search took {time.time() - dense_start:.3f}s")

            if mode in ["sparse", "hybrid", "hybrid_rerank"]:
                sparse_start = time.time()
                sparse_results = sparse_retriever.search_sparse(query, top_k=settings.rag.bm25_top_k)
                logger.debug(f"Sparse search took {time.time() - sparse_start:.3f}s")
                
            if mode == "dense":
                final_results = dense_results[:top_k]
            elif mode == "sparse":
                final_results = sparse_results[:top_k]
            elif mode in ["hybrid", "hybrid_rerank"]:
                fusion_start = time.time()
                fused = reciprocal_rank_fusion(dense_results, sparse_results)
                logger.debug(f"Fusion took {time.time() - fusion_start:.3f}s")
                
                if mode == "hybrid_rerank":
                    rerank_start = time.time()
                    final_results = reranker_layer.rerank(query, fused, top_n=top_k)
                    logger.debug(f"Reranking took {time.time() - rerank_start:.3f}s")
                else:
                    final_results = fused[:top_k]
                    
            total_time = time.time() - start_time
            logger.info(f"Retrieval complete in {total_time:.3f}s | Mode: {mode} | Returned: {len(final_results)}")
            
            return {
                "mode": mode,
                "latency_sec": total_time,
                "results": final_results
            }
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            raise

retriever = Retriever()
