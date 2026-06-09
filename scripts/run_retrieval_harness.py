import json
import sys
from pathlib import Path
import time
from src.llm_ops.core.logging import setup_logging, get_logger
from src.llm_ops.core.config import settings
from src.llm_ops.rag.retriever import retriever

setup_logging()
logger = get_logger(__name__)

def evaluate_queries(dataset_path: Path):
    if not dataset_path.exists():
        logger.error(f"Eval dataset not found: {dataset_path}")
        sys.exit(1)
        
    queries = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                queries.append(json.loads(line))
                
    results_log = []
    
    total_queries = len(queries)
    hits_at_k = 0
    total_mrr = 0.0
    total_precision = 0.0
    total_recall = 0.0
    metadata_valid_count = 0
    must_contain_hits = 0
    
    for q_data in queries:
        query = q_data["query"]
        expected_sources = set(q_data.get("expected_sources", []))
        must_contain = set(q_data.get("must_contain", []))
        
        try:
            ret = retriever.retrieve(query)
            results = ret["results"]
            
            returned_sources = []
            valid_meta = True
            all_terms_found = set()
            
            first_hit_rank = None
            
            for rank, r in enumerate(results):
                meta = r["payload"].get("metadata", {})
                source = Path(meta.get("source_path", "")).name
                returned_sources.append(source)
                
                if "doc_id" not in meta or "chunk_id" not in meta:
                    valid_meta = False
                    
                text_lower = r["payload"].get("text", "").lower()
                for term in must_contain:
                    if term.lower() in text_lower:
                        all_terms_found.add(term)
                        
                if first_hit_rank is None and source in expected_sources:
                    first_hit_rank = rank + 1
                    
            if valid_meta:
                metadata_valid_count += 1
                
            if len(all_terms_found) == len(must_contain):
                must_contain_hits += 1
                
            # Hit rate & MRR
            if first_hit_rank is not None:
                hits_at_k += 1
                total_mrr += 1.0 / first_hit_rank
                
            # Precision & Recall
            if len(expected_sources) > 0:
                ret_set = set(returned_sources)
                intersection = ret_set.intersection(expected_sources)
                
                recall = len(intersection) / len(expected_sources)
                total_recall += recall
                
                precision = len(intersection) / len(ret_set) if len(ret_set) > 0 else 0.0
                total_precision += precision
                
            results_log.append({
                "id": q_data["id"],
                "query": query,
                "latency_sec": ret["latency_sec"],
                "found_expected": first_hit_rank is not None,
                "first_hit_rank": first_hit_rank
            })
            
        except Exception as e:
            logger.error(f"Failed query eval: {e}")
            
    metrics = {
        "mode": settings.rag.rag_mode,
        "reranker_enabled": settings.reranker.reranker_enabled,
        "qdrant_hybrid": settings.qdrant.qdrant_use_hybrid,
        "total_queries": total_queries,
        "recall_at_5": total_recall / total_queries if total_queries > 0 else 0,
        "precision_at_5": total_precision / total_queries if total_queries > 0 else 0,
        "mrr": total_mrr / total_queries if total_queries > 0 else 0,
        "source_hit_rate": hits_at_k / total_queries if total_queries > 0 else 0,
        "must_contain_hit_rate": must_contain_hits / total_queries if total_queries > 0 else 0,
        "metadata_validity_rate": metadata_valid_count / total_queries if total_queries > 0 else 0
    }
    
    return metrics, results_log

def main():
    dataset_path = Path(settings.rag.retrieval_eval_dataset)
    metrics, results_log = evaluate_queries(dataset_path)
    
    report_dir = Path(settings.rag.retrieval_report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    mode_name = settings.rag.rag_mode
    json_path = report_dir / f"retrieval_harness_{mode_name}.json"
    
    report_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metrics": metrics,
        "results": results_log
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    logger.info(f"Report written to {json_path}")
    logger.info(f"Metrics: {json.dumps(metrics, indent=2)}")
    
    # Assert constraints
    assert metrics["recall_at_5"] >= settings.rag.min_retrieval_recall_at_5, "Recall too low"
    assert metrics["precision_at_5"] >= settings.rag.min_retrieval_precision_at_5, "Precision too low"
    assert metrics["metadata_validity_rate"] == 1.0, "Metadata invalid"

if __name__ == "__main__":
    main()
