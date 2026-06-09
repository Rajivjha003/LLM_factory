import pickle
import json
from pathlib import Path
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import get_logger
from src.llm_ops.rag.chunking import DocumentChunk

logger = get_logger(__name__)

class SparseRetriever:
    def __init__(self):
        self.bm25 = None
        self.corpus = []
        self.chunk_ids = []
        self.metadata_store = {}
        self.index_path = Path(settings.rag.bm25_index_path)
        self.manifest_path = Path(settings.rag.bm25_manifest_path)
        
    def _tokenize(self, text: str) -> List[str]:
        # Simple whitespace and lowercase tokenizer
        return text.lower().split()
        
    def build_index(self, chunks: List[DocumentChunk]):
        if not chunks:
            logger.warning("Attempted to build sparse index with 0 chunks.")
            return
            
        tokenized_corpus = []
        self.corpus = []
        self.chunk_ids = []
        self.metadata_store = {}
        
        for c in chunks:
            self.corpus.append(c.content)
            self.chunk_ids.append(c.metadata.chunk_id)
            self.metadata_store[c.metadata.chunk_id] = json.loads(c.metadata.model_dump_json())
            tokenized_corpus.append(self._tokenize(c.content))
            
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.info(f"Built BM25 index with {len(self.corpus)} chunks.")
        
    def save_index(self):
        if self.bm25 is None:
            logger.error("No BM25 index to save.")
            return
            
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump({
                "corpus": self.corpus,
                "chunk_ids": self.chunk_ids,
                "metadata_store": self.metadata_store
            }, f)
            
        manifest = {
            "num_chunks": len(self.corpus),
            "tokenizer": "whitespace_lower"
        }
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            
        logger.info(f"Saved BM25 index to {self.index_path}")
        
    def load_index(self):
        if not self.index_path.exists():
            logger.error(f"BM25 index not found at {self.index_path}")
            return False
            
        try:
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)
                
            self.corpus = data["corpus"]
            self.chunk_ids = data["chunk_ids"]
            self.metadata_store = data.get("metadata_store", {})
            
            tokenized_corpus = [self._tokenize(c) for c in self.corpus]
            self.bm25 = BM25Okapi(tokenized_corpus)
            logger.info(f"Loaded BM25 index with {len(self.corpus)} chunks.")
            return True
        except Exception as e:
            logger.error(f"Failed to load BM25 index: {e}")
            return False
            
    def search_sparse(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        if self.bm25 is None:
            if not self.load_index():
                return []
                
        if top_k is None:
            top_k = settings.rag.bm25_top_k
            
        tokenized_query = self._tokenize(query)
        doc_scores = self.bm25.get_scores(tokenized_query)
        
        # Sort and get top_k
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            score = doc_scores[idx]
            if score <= 0.0:
                continue # BM25 drops non-matches to 0
                
            chunk_id = self.chunk_ids[idx]
            results.append({
                "id": chunk_id,
                "score": score,
                "payload": {
                    "text": self.corpus[idx],
                    "metadata": self.metadata_store.get(chunk_id, {})
                }
            })
            
        return results

sparse_retriever = SparseRetriever()
