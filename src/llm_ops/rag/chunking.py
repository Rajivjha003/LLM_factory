from typing import List, Dict, Any
import hashlib
import os
import datetime
import uuid
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
from src.llm_ops.rag.metadata import ChunkMetadata

logger = get_logger(__name__)

class DocumentChunk:
    def __init__(self, content: str, metadata: ChunkMetadata):
        self.content = content
        self.metadata = metadata

class ChunkingPolicy:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        
    def _create_metadata(self, source_path: str, chunk_index: int, content: str) -> ChunkMetadata:
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        _, ext = os.path.splitext(source_path)
        
        return ChunkMetadata(
            doc_id=hashlib.md5(source_path.encode('utf-8')).hexdigest(),
            source_path=source_path,
            source_type=ext if ext else "unknown",
            domain="general",
            client="merchmix",
            phase=settings.app.app_env,
            created_at=datetime.datetime.utcnow().isoformat(),
            updated_at=datetime.datetime.utcnow().isoformat(),
            chunk_id=str(uuid.uuid4()),
            chunk_index=chunk_index,
            hash=content_hash,
            tags=[]
        )

    def process_file(self, file_path: str) -> List[DocumentChunk]:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise e
            
        _, ext = os.path.splitext(file_path)
        
        if ext == '.md':
            return self.chunk_markdown(file_path, content)
        elif ext == '.sql':
            return self.chunk_sql(file_path, content)
        elif ext == '.py':
            return self.chunk_python(file_path, content)
        else:
            return self.chunk_generic(file_path, content)

    def chunk_markdown(self, source_path: str, text: str) -> List[DocumentChunk]:
        # Minimal viable chunking by newlines/size for now
        return self.chunk_generic(source_path, text)
        
    def chunk_sql(self, source_path: str, sql: str) -> List[DocumentChunk]:
        return self.chunk_generic(source_path, sql)
        
    def chunk_python(self, source_path: str, code: str) -> List[DocumentChunk]:
        return self.chunk_generic(source_path, code)
        
    def chunk_generic(self, source_path: str, text: str) -> List[DocumentChunk]:
        chunks = []
        start = 0
        text_len = len(text)
        index = 0
        
        if text_len == 0:
            return []
            
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            # Simple boundary check to avoid splitting words
            if end < text_len:
                while end > start and not text[end-1].isspace():
                    end -= 1
                if end == start:
                    end = min(start + self.chunk_size, text_len)
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                metadata = self._create_metadata(source_path, index, chunk_text)
                chunks.append(DocumentChunk(content=chunk_text, metadata=metadata))
                index += 1
                
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
            if start >= end:
                start = end
                
        return chunks
