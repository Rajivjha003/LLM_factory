import pytest
from src.llm_ops.rag.sparse_retriever import sparse_retriever
from src.llm_ops.rag.chunking import DocumentChunk
from src.llm_ops.rag.metadata import ChunkMetadata

def test_sparse_retriever_build_and_search():
    meta = ChunkMetadata(
        doc_id="d1", source_path="f1", source_type="txt", domain="d", client="c",
        phase="p", created_at="1", updated_at="1", chunk_id="c1", chunk_index=0, hash="h1", tags=[]
    )
    c1 = DocumentChunk("This is a sparse search test document", meta)
    
    meta2 = ChunkMetadata(
        doc_id="d2", source_path="f2", source_type="txt", domain="d", client="c",
        phase="p", created_at="1", updated_at="1", chunk_id="c2", chunk_index=0, hash="h2", tags=[]
    )
    c2 = DocumentChunk("Completely unrelated content about Qdrant and vectors", meta2)
    
    sparse_retriever.build_index([c1, c2])
    
    results = sparse_retriever.search_sparse("sparse search test")
    
    assert len(results) > 0
    assert results[0]["id"] == "c1"
    assert results[0]["score"] > 0
