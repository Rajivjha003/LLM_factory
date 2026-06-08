from pydantic import BaseModel, Field
from typing import List, Optional

class ChunkMetadata(BaseModel):
    doc_id: str
    source_path: str
    source_type: str
    domain: str
    client: str
    phase: str
    created_at: str
    updated_at: str
    chunk_id: str
    chunk_index: int
    hash: str
    tags: List[str] = Field(default_factory=list)
