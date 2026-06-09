import pytest
from src.llm_ops.rag.chunking import ChunkingPolicy

def test_deterministic_chunking_ids():
    policy = ChunkingPolicy()
    
    content = "This is a test document."
    source_path = "data/rag_corpus/test_doc.md"
    
    chunks1 = policy.chunk_generic(source_path, content)
    chunks2 = policy.chunk_generic(source_path, content)
    
    assert chunks1[0].metadata.chunk_id == chunks2[0].metadata.chunk_id
    assert chunks1[0].metadata.doc_id == chunks2[0].metadata.doc_id
