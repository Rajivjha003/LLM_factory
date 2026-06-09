import argparse
import os
import time
import json
from pathlib import Path
import hashlib
from typing import Dict, List, Any

from src.llm_ops.core.config import settings
from src.llm_ops.core.logging import setup_logging, get_logger
from src.llm_ops.rag.chunking import ChunkingPolicy
from src.llm_ops.rag.embeddings import embedding_layer
from src.llm_ops.rag.qdrant_store import qdrant_store
from src.llm_ops.rag.sparse_retriever import sparse_retriever

setup_logging()
logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {'.md', '.txt', '.sql', '.py', '.json', '.jsonl', '.yaml', '.yml'}
MAX_FILE_SIZE_BYTES = settings.rag.rag_max_file_size_mb * 1024 * 1024

def scan_corpus(source_dir: str) -> List[str]:
    valid_files = []
    base_path = Path(source_dir)
    if not base_path.exists():
        logger.error(f"Source dir not found: {source_dir}")
        return []
        
    for root, _, files in os.walk(base_path):
        # Ignore noisy dirs
        if any(ignored in root for ignored in ['.venv', '.git', '__pycache__', 'node_modules', 'data/qdrant']):
            continue
            
        for file in files:
            path = Path(root) / file
            if path.suffix.lower() in ALLOWED_EXTENSIONS:
                if path.stat().st_size <= MAX_FILE_SIZE_BYTES:
                    valid_files.append(str(path))
                else:
                    logger.warning(f"File skipped (exceeds max size): {path}")
            else:
                logger.debug(f"File skipped (unsupported extension): {path}")
    return valid_files

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into Qdrant")
    parser.add_argument("--source", type=str, default=settings.rag.rag_corpus_dir, help="Source directory for corpus")
    parser.add_argument("--reset-collection", action="store_true", help="Reset Qdrant collection before ingestion")
    args = parser.parse_args()

    run_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
    logger.info(f"Starting ingestion run {run_id} from {args.source}")
    
    if args.reset_collection:
        logger.info(f"Attempting to reset collection {settings.qdrant.qdrant_collection_docs}...")
        qdrant_store.delete_collection_if_allowed(settings.qdrant.qdrant_collection_docs, force=True)

    qdrant_store.ensure_collection(
        collection_name=settings.qdrant.qdrant_collection_docs,
        vector_size=settings.qdrant.qdrant_vector_size
    )

    valid_files = scan_corpus(args.source)
    if not valid_files:
        logger.error("No valid files found for ingestion.")
        return

    chunking_policy = ChunkingPolicy()
    
    files_seen = len(valid_files)
    files_ingested = 0
    files_failed = 0
    chunks_created = 0
    chunks_upserted = 0
    failed_files = []
    file_hashes = {}
    all_chunks = []
    
    start_time = time.time()
    
    for file_path in valid_files:
        try:
            logger.info(f"Processing {file_path}")
            chunks = chunking_policy.process_file(file_path)
            if not chunks:
                logger.warning(f"No chunks produced from {file_path}")
                continue
                
            texts = [c.content for c in chunks]
            embeddings = embedding_layer.embed_documents(texts)
            
            qdrant_store.upsert_chunks(
                collection_name=settings.qdrant.qdrant_collection_docs,
                chunks=chunks,
                embeddings=embeddings
            )
            
            files_ingested += 1
            chunks_created += len(chunks)
            chunks_upserted += len(chunks)
            all_chunks.extend(chunks)
            
            # Simple hash record for manifest
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                file_hashes[file_path] = hashlib.sha256(content.encode()).hexdigest()
                
        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {e}")
            files_failed += 1
            failed_files.append(file_path)
            
    if settings.rag.sparse_retrieval_enabled and all_chunks:
        logger.info("Building BM25 sparse index...")
        sparse_retriever.build_index(all_chunks)
        sparse_retriever.save_index()
            
    duration_seconds = time.time() - start_time
    
    manifest = {
        "run_id": run_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_dir": args.source,
        "collection_name": settings.qdrant.qdrant_collection_docs,
        "embedding_model": settings.embedding.embedding_model,
        "vector_size": settings.qdrant.qdrant_vector_size,
        "files_seen": files_seen,
        "files_ingested": files_ingested,
        "files_failed": files_failed,
        "chunks_created": chunks_created,
        "chunks_upserted": chunks_upserted,
        "failed_files": failed_files,
        "file_hashes": file_hashes,
        "duration_seconds": duration_seconds
    }
    
    manifest_path = Path(settings.rag.rag_ingest_manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    logger.info(f"Ingestion complete in {duration_seconds:.2f}s. Manifest written to {manifest_path}")

if __name__ == "__main__":
    main()
