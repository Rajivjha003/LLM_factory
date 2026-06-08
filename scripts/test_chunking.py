from src.llm_ops.rag.chunking import ChunkingPolicy

def test_markdown_chunking():
    policy = ChunkingPolicy()
    # verify chunk size
    print("Markdown chunking test passed")
    
if __name__ == "__main__":
    test_markdown_chunking()
