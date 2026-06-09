import pytest
import uuid
from src.llm_ops.rag.qdrant_store import qdrant_store
from src.llm_ops.core.exceptions import RetrievalError
from src.llm_ops.rag.chunking import DocumentChunk
from src.llm_ops.rag.metadata import ChunkMetadata
from src.llm_ops.core.config import settings

@pytest.mark.integration
def test_qdrant_health_check():
    assert qdrant_store.health_check() is True

@pytest.mark.integration
def test_qdrant_upsert_and_search():
    collection_name = "test_integration_docs"
    qdrant_store.ensure_collection(collection_name, 768)
    
    dummy_meta = ChunkMetadata(
        doc_id="test_doc",
        source_path="test.md",
        source_type="md",
        domain="test",
        client="test",
        phase="test",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        chunk_id=str(uuid.uuid4()),
        chunk_index=0,
        hash="testhash",
        tags=[]
    )
    chunk = DocumentChunk(content="Test content", metadata=dummy_meta)
    vector = [0.1] * 768
    
    qdrant_store.upsert_chunks(collection_name, [chunk], [vector])
    
    # Allow some time for indexing if necessary, though qdrant is quite fast
    results = qdrant_store.search_dense(collection_name, vector, top_k=1)
    
    assert len(results) > 0
    assert results[0]["payload"]["text"] == "Test content"
