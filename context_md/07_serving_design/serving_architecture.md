# Serving Architecture

## Architecture
User/App -> FastAPI Gateway -> Model Router -> Backend

Backends:
- llama.cpp for GGUF local inference
- vLLM for OpenAI-compatible GPU serving

## Gateway Responsibilities
- Auth
- Request validation
- Prompt template selection
- Model routing
- Streaming
- Logging
- Safety checks
