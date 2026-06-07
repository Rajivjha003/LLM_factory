# RAG Document Schema

## Purpose
Make project facts retrievable without baking everything into model weights.

## Schema
```json
{
  "doc_id": "doc_000001",
  "title": "WSSI Metric Definitions",
  "source": "project_document",
  "version": "v1",
  "chunk_id": "doc_000001_chunk_001",
  "text": "Document chunk here.",
  "metadata": {
    "domain": "retail_metrics",
    "client": "redacted_or_allowed",
    "created_at": "YYYY-MM-DD"
  }
}
```

## Chunking Rules
- Keep chunks semantically complete.
- Include table/schema names in metadata.
- Preserve source title.
- Avoid mixing unrelated concepts.
