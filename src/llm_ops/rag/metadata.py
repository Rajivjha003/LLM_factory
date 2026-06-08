from pydantic import BaseModel, Field
from typing import List, Optional

class ChunkMetadata(BaseModel):
    doc_id: str = Field(..., description="Unique document ID")
    source_path: str = Field(..., description="Original file path or URL")
    source_type: str = Field(..., description="File extension or source type (e.g. .py, .md)")
    domain: str = Field(..., description="Domain of the knowledge (e.g. code, docs, tickets)")
    client: str = Field(..., description="Client or tenant name")
    phase: str = Field(..., description="Current phase or environment")
    created_at: str = Field(..., description="Creation timestamp ISO")
    updated_at: str = Field(..., description="Last updated timestamp ISO")
    chunk_id: str = Field(..., description="Unique ID for this specific chunk")
    chunk_index: int = Field(..., description="Index of this chunk in the document")
    hash: str = Field(..., description="SHA-256 hash of the chunk content for deduplication")
    tags: List[str] = Field(default_factory=list, description="Categorical tags")
