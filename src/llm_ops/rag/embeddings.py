import torch
from sentence_transformers import SentenceTransformer
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
import math

logger = get_logger(__name__)

class EmbeddingLayer:
    def __init__(self):
        self.model = None
        self.device = None
        
    def load_model(self):
        if self.model is not None:
            return
            
        target_device = settings.embedding.embedding_device
        if target_device == "cuda" and not torch.cuda.is_available():
            if settings.embedding.embedding_allow_cpu_fallback:
                logger.warning("CUDA requested but not available. Falling back to CPU for embeddings.")
                target_device = "cpu"
            else:
                logger.error("CUDA is not available and CPU fallback is disabled.")
                raise RuntimeError("CUDA not available for embeddings.")
                
        self.device = target_device
        logger.info(f"Loading embedding model: {settings.embedding.embedding_model} on {self.device}")
        try:
            self.model = SentenceTransformer(settings.embedding.embedding_model, device=self.device)
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise e

    def get_vector_size(self) -> int:
        self.load_model()
        return self.model.get_sentence_embedding_dimension()
        
    def _validate_texts(self, texts: list[str]):
        if not texts:
            raise ValueError("Input texts list cannot be empty.")
        for text in texts:
            if not isinstance(text, str):
                raise TypeError("Input texts must be strings.")
            if not text.strip():
                raise ValueError("Input texts cannot contain empty strings.")

    def _validate_vectors(self, vectors):
        import numpy as np
        if np.isnan(vectors).any() or np.isinf(vectors).any():
            raise ValueError("Embeddings generated NaN or Inf values.")
            
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.load_model()
        self._validate_texts(texts)
        
        logger.debug(f"Embedding {len(texts)} documents in batch size {settings.embedding.embedding_batch_size}")
        embeddings = self.model.encode(
            texts, 
            batch_size=settings.embedding.embedding_batch_size, 
            show_progress_bar=False,
            normalize_embeddings=True
        )
        self._validate_vectors(embeddings)
        return embeddings.tolist()
        
    def embed_query(self, text: str) -> list[float]:
        self.load_model()
        self._validate_texts([text])
        
        embedding = self.model.encode(
            [text], 
            batch_size=1, 
            show_progress_bar=False,
            normalize_embeddings=True
        )[0]
        self._validate_vectors(embedding)
        return embedding.tolist()

# Singleton instance
embedding_layer = EmbeddingLayer()
