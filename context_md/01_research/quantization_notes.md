# Quantization Notes

## Training Quantization
Use QLoRA with NF4 4-bit for local fine-tuning.

## Local Inference Quantization
Use GGUF for llama.cpp.

Recommended order:
1. Q4_K_M: baseline speed/size.
2. Q5_K_M: better quality.
3. Q8_0: near-full quality, larger.

## API Serving Quantization
Use vLLM-compatible quantization where supported:
- AWQ
- GPTQ
- FP8
- INT8/INT4 depending model and hardware support

## Policy
Do not assume one quantization format is universally best. Always benchmark quality, latency, and memory.
