import pytest
from src.llm_ops.rag.fusion import reciprocal_rank_fusion

def test_rrf():
    dense = [
        {"id": "a", "score": 0.9, "payload": {}},
        {"id": "b", "score": 0.8, "payload": {}},
        {"id": "c", "score": 0.7, "payload": {}},
    ]
    
    sparse = [
        {"id": "c", "score": 10.5, "payload": {}},
        {"id": "b", "score": 8.0, "payload": {}},
        {"id": "d", "score": 7.0, "payload": {}},
    ]
    
    # RRF formula: 1 / (60 + rank+1)
    fused = reciprocal_rank_fusion(dense, sparse)
    
    assert len(fused) == 4
    
    # chunk 'c' has rank 3 in dense, rank 1 in sparse
    # chunk 'b' has rank 2 in dense, rank 2 in sparse
    # Let's just ensure we return all unique elements and scores exist
    ids = [r["id"] for r in fused]
    assert set(ids) == {"a", "b", "c", "d"}
    
    for r in fused:
        assert "score" in r
        assert "dense_score" in r
        assert "sparse_score" in r
