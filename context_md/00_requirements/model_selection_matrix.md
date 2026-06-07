# Model Selection Matrix

## Selection Criteria
A model is eligible only if it satisfies most of the following:

- License allows intended use.
- Fits RTX 4090 Laptop 16 GB VRAM with QLoRA.
- Supported by Unsloth or compatible with Transformers/PEFT.
- Supported by vLLM or has known serving path.
- Convertible to GGUF for llama.cpp.
- Strong tokenizer for code, SQL, and structured output.
- Has stable chat template.
- Has active community support.
- Has good reasoning/coding baseline.

## Model Lanes
| Lane | Size | Purpose |
|---|---:|---|
| Tiny scratch | 30M-300M | Learn internals |
| Speed lab | 0.5B-1.5B | Rapid iteration |
| Main lab | 3B | Best local speed/quality iteration |
| Serious local | 7B-8B | Main production-quality fine-tuning |
| Stretch local | 14B | Experimental |
| Cloud later | 32B+ | Future scale |

## Recommended Strategy
1. Start with 1.5B/3B for pipeline validation.
2. Move to 7B/8B for serious SFT/DPO/GRPO.
3. Keep a tiny model path for architecture learning.
4. Do not begin with 14B.
