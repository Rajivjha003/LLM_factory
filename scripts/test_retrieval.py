import json
import sys
from pathlib import Path
from src.llm_ops.core.logging import setup_logging, get_logger
from src.llm_ops.core.config import settings
from src.llm_ops.rag.embeddings import embedding_layer
from src.llm_ops.rag.qdrant_store import qdrant_store

setup_logging()
logger = get_logger(__name__)

def main():
    eval_file = Path("data/eval/retrieval_smoke_v1.jsonl")
    if not eval_file.exists():
        logger.error(f"Smoke eval file not found: {eval_file}")
        sys.exit(1)
        
    queries = []
    with open(eval_file, "r") as f:
        for line in f:
            if line.strip():
                queries.append(json.loads(line))
                
    success_count = 0
    
    for q_data in queries:
        query = q_data["query"]
        must_contain = q_data["must_contain"]
        top_k = q_data.get("top_k", 5)
        
        logger.info(f"Query: {query}")
        query_vector = embedding_layer.embed_query(query)
        
        results = qdrant_store.search_dense(
            collection_name=settings.qdrant.qdrant_collection_docs,
            query_vector=query_vector,
            top_k=top_k
        )
        
        if not results:
            logger.error(f"No results returned for query: {query}")
            sys.exit(1)
            
        found_all = True
        matched_terms_overall = set()
        
        for i, res in enumerate(results):
            text = res["payload"].get("text", "")
            meta = res["payload"].get("metadata", {})
            score = res.get("score", 0.0)
            
            # Simple term matching (case insensitive)
            text_lower = text.lower()
            matched_terms = [t for t in must_contain if t.lower() in text_lower]
            matched_terms_overall.update(matched_terms)
            
            logger.info(f"  Rank: {i+1} | Score: {score:.4f} | Chunk ID: {meta.get('chunk_id')}")
            logger.info(f"  Source: {meta.get('source_path')}")
            logger.info(f"  Matched terms in chunk: {matched_terms}")
            logger.info(f"  Preview: {text[:100]}...\n")
            
        missing_terms = [t for t in must_contain if t not in matched_terms_overall]
        if missing_terms:
            logger.error(f"Query failed to retrieve evidence for terms: {missing_terms}")
            found_all = False
        else:
            success_count += 1
            
    if success_count == len(queries):
        logger.info(f"Retrieval smoke test PASSED ({success_count}/{len(queries)})")
        sys.exit(0)
    else:
        logger.error(f"Retrieval smoke test FAILED ({success_count}/{len(queries)})")
        sys.exit(1)

if __name__ == "__main__":
    main()
