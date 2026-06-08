import os
from src.llm_ops.rag.chunking import ChunkingPolicy
from src.llm_ops.rag.metadata import ChunkMetadata

def test_markdown_chunking():
    policy = ChunkingPolicy()
    
    # Create a dummy markdown file
    dummy_file = "test_dummy.md"
    content = "# Title\n\nThis is a test document. " * 50
    with open(dummy_file, "w") as f:
        f.write(content)
        
    chunks = policy.process_file(dummy_file)
    
    # Verify chunks are created
    assert len(chunks) > 0
    
    # Verify metadata strictly adheres to schema
    first_chunk = chunks[0]
    assert isinstance(first_chunk.metadata, ChunkMetadata)
    assert first_chunk.metadata.source_path == dummy_file
    assert first_chunk.metadata.source_type == ".md"
    assert first_chunk.metadata.hash is not None
    assert first_chunk.content is not None
    
    # Clean up
    os.remove(dummy_file)
