import pytest
from src.llm_ops.rag.reranker import reranker_layer

@pytest.mark.gpu
def test_reranker():
    query = "What is the capital of France?"
    candidates = [
        {"id": "1", "score": 0.5, "payload": {"text": "The capital of France is Paris."}},
        {"id": "2", "score": 0.9, "payload": {"text": "Berlin is the capital of Germany."}}
    ]
    
    reranked = reranker_layer.rerank(query, candidates)
    
    # Paris should be boosted to top
    assert reranked[0]["id"] == "1"
    assert reranked[0]["rerank_score"] > reranked[1]["rerank_score"]
