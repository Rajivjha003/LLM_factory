import pytest
from src.llm_ops.rag.embeddings import embedding_layer

@pytest.mark.gpu
def test_embedding_model_loads_and_embeds():
    # Test single query embedding
    emb = embedding_layer.embed_query("Hello world")
    assert len(emb) == 768
    
    # Test batch embedding
    embs = embedding_layer.embed_documents(["Doc 1", "Doc 2"])
    assert len(embs) == 2
    assert len(embs[0]) == 768
    
def test_embedding_validation_rejects_empty():
    with pytest.raises(ValueError):
        embedding_layer._validate_texts([])
        
    with pytest.raises(ValueError):
        embedding_layer._validate_texts([""])
