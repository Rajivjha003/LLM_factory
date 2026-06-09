from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
from src.llm_ops.core.exceptions import RetrievalError, ValidationError
import httpx
import json

logger = get_logger(__name__)

class QdrantStore:
    def __init__(self):
        self.url = settings.qdrant.qdrant_url
        self.api_key = settings.qdrant.qdrant_api_key
        try:
            self.client = QdrantClient(url=self.url, api_key=self.api_key if self.api_key else None)
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise RetrievalError(f"Qdrant initialization failed: {e}")
            
    def health_check(self) -> bool:
        try:
            response = httpx.get(f"{self.url}/healthz", timeout=5.0)
            if response.status_code == 200:
                return True
            return False
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            raise RetrievalError(f"Qdrant is not reachable at {self.url}")
            
    def ensure_collection(self, collection_name: str, vector_size: int = 768):
        self.health_check()
        
        try:
            collections_response = self.client.get_collections()
            exists = any(c.name == collection_name for c in collections_response.collections)
            
            if exists:
                info = self.client.get_collection(collection_name)
                # Qdrant v1.7+ nested params might differ, let's carefully check vector size
                # Handle possible different vector config types
                vector_config = info.config.params.vectors
                existing_size = None
                if isinstance(vector_config, qmodels.VectorParams):
                    existing_size = vector_config.size
                elif isinstance(vector_config, dict) and "size" in vector_config:
                    existing_size = vector_config["size"]
                elif hasattr(vector_config, "size"):
                    existing_size = vector_config.size
                    
                if existing_size is not None and existing_size != vector_size:
                    raise RetrievalError(f"Collection {collection_name} exists but vector size {existing_size} != required {vector_size}")
                logger.info(f"Collection {collection_name} exists and vector size is valid.")
                return
                
            logger.info(f"Creating new collection {collection_name} with size {vector_size}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=qmodels.VectorParams(
                    size=vector_size,
                    distance=qmodels.Distance.COSINE
                )
            )
        except RetrievalError:
            raise
        except Exception as e:
            logger.error(f"Failed to ensure collection {collection_name}: {e}")
            raise RetrievalError(f"Ensure collection failed: {e}")
            
    def get_collection_info(self, collection_name: str) -> dict:
        self.health_check()
        try:
            info = self.client.get_collection(collection_name)
            return {"status": info.status, "points_count": info.points_count}
        except Exception as e:
            logger.error(f"Failed to get collection info for {collection_name}: {e}")
            raise RetrievalError(f"Get collection info failed: {e}")
            
    def delete_collection_if_allowed(self, collection_name: str, force: bool = False):
        if not force:
            logger.warning(f"Delete collection {collection_name} blocked: force flag not set")
            return
            
        if settings.app.app_env != "local":
            logger.error("Auto-delete of collections is strictly forbidden outside 'local' app environment.")
            raise RetrievalError("Delete collection blocked by safety constraints.")
            
        self.health_check()
        try:
            self.client.delete_collection(collection_name=collection_name)
            logger.info(f"Successfully deleted collection {collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection {collection_name}: {e}")
            raise RetrievalError(f"Delete collection failed: {e}")

    def upsert_chunks(self, collection_name: str, chunks: list, embeddings: list[list[float]]):
        self.health_check()
        if not chunks or not embeddings:
            raise ValidationError("Cannot upsert empty chunks or embeddings.")
        if len(chunks) != len(embeddings):
            raise ValidationError("Chunks and embeddings length mismatch.")
            
        points = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            if not chunk.content or not chunk.content.strip():
                raise ValidationError(f"Chunk {i} has empty content.")
            if len(emb) != settings.qdrant.qdrant_vector_size:
                raise RetrievalError(f"Vector dimension {len(emb)} != required {settings.qdrant.qdrant_vector_size}")
            
            # Validate strict metadata
            try:
                meta_dict = json.loads(chunk.metadata.model_dump_json())
            except Exception as e:
                raise ValidationError(f"Invalid metadata format: {e}")
            
            payload = {
                "text": chunk.content,
                "metadata": meta_dict
            }
            
            points.append(qmodels.PointStruct(
                id=chunk.metadata.chunk_id,
                vector=emb,
                payload=payload
            ))
            
        try:
            logger.info(f"Upserting {len(points)} points into {collection_name}")
            self.client.upsert(
                collection_name=collection_name,
                points=points
            )
        except Exception as e:
            logger.error(f"Upsert failed: {e}")
            raise RetrievalError(f"Upsert chunks failed: {e}")

    def search_dense(self, collection_name: str, query_vector: list[float], top_k: int = 5) -> list[dict]:
        self.health_check()
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "id": r.id,
                    "score": r.score,
                    "payload": r.payload
                })
            return formatted_results
        except Exception as e:
            logger.error(f"Dense search failed: {e}")
            raise RetrievalError(f"Dense search failed: {e}")

qdrant_store = QdrantStore()
