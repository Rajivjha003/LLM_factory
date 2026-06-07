# Stack Decisions

## Default Python Version
Python 3.11.

## OS
WSL2 Ubuntu 24.04.

## Environment Manager
uv.

## Core Training Stack
- PyTorch
- Transformers
- Datasets
- Accelerate
- PEFT
- TRL
- Unsloth
- bitsandbytes

## Serving Stack
- llama.cpp for GGUF local inference
- vLLM for OpenAI-compatible API inference
- FastAPI as gateway

## RAG Stack
- Qdrant or pgvector
- BGE/Jina embedding models
- Reranker
- Ragas/custom evals

## Agent Stack
- MCP-style tool contracts
- Custom planner/router/verifier
- Sandbox and permission system

## Observability
- Langfuse or Phoenix for LLM traces
- Prometheus/Grafana for infrastructure metrics
- MLflow or W&B for experiment tracking

## Principle
Unsloth-first, not Unsloth-only. Keep compatibility with the broader Hugging Face ecosystem.
