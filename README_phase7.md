# Phase 7 — Champion Packaging, Quantization, and Local Inference Benchmarking

## Objective

Your current champion is:

- Base: Qwen2.5-1.5B-Instruct
- Champion adapter: `artifacts/adapters/qwen_1_5b_sft_v2_failure_driven`
- Merged champion: `artifacts/merged/qwen_1_5b_sft_v2_merged`
- Frozen eval: `data/eval_v3`
- Judge: Judge v3 + SQL verifier

Phase 7 converts the champion from a research artifact into deployable model artifacts.

## What Phase 7 produces

- Verified merged Hugging Face model
- Champion model card
- Model package manifest
- HF inference benchmark
- Judge v3 regression evaluation on merged model
- llama.cpp setup
- GGUF conversion
- Q8_0, Q5_K_M, Q4_K_M quantized models
- llama.cpp speed benchmark
- quantized model quality smoke test
- final promotion registry

## Run order

```bash
cd ~/LLM_Ops
source .venv/bin/activate

unzip /path/to/phase7_packaging_quantization_package.zip -d .
chmod +x scripts/phase7_end_to_end.sh
chmod +x scripts/setup_llama_cpp.sh
chmod +x scripts/convert_and_quantize_champion_gguf.sh
chmod +x scripts/benchmark_llama_cpp_quantized.sh

./scripts/phase7_end_to_end.sh
```

## Promotion rule

A quantized artifact is allowed for local use if:

1. Merged HF model loads successfully.
2. Merged model Judge v3 eval does not regress against known champion behavior.
3. GGUF conversion succeeds.
4. Quantized model can generate a sane Merchmix answer.
5. Q4_K_M / Q5_K_M speed is acceptable.
6. No destructive SQL is generated inside executable SQL blocks in smoke tests.

## Recommended default artifact

For local CPU/GPU-light inference:

- `models/gguf/qwen_1_5b_sft_v2_merged.Q5_K_M.gguf`

For best quality:

- `models/gguf/qwen_1_5b_sft_v2_merged.Q8_0.gguf`

For smallest/fastest:

- `models/gguf/qwen_1_5b_sft_v2_merged.Q4_K_M.gguf`

