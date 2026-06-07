# AWQ/GPTQ Strategy

## Purpose
Weight quantization for efficient vLLM-compatible serving.

## Use When
- vLLM supports the model/format.
- GGUF is not the desired API serving path.
- Latency/VRAM requires compression.

## Validate
- Domain eval
- SQL eval
- Safety eval
- Latency eval
