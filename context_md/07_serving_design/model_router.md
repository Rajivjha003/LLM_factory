# Model Router

## Purpose
Route requests to the correct backend/model.

## Routing Factors
- Task type
- Model size
- Latency requirement
- RAG required or not
- Tool use required or not
- Local GGUF vs vLLM API

## Example
- Simple local chat -> llama.cpp Q4_K_M
- SQL reasoning -> 7B DPO/GRPO model
- API workload -> vLLM
