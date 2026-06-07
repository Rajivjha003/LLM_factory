# Project Charter

## Purpose
To develop a robust, high-performance LLM operations pipeline that seamlessly handles model fine-tuning, quantization, evaluation, and deployment, prioritizing local execution where possible and taking full advantage of the available hardware.

## Scope
- Base model retrieval and caching.
- Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO).
- Group Relative Policy Optimization (GRPO).
- Model quantization (e.g., GGUF, AWQ, FP8) to minimize footprint and maximize throughput.
- High-performance inference and serving using standard tools like vLLM.
- Evaluation frameworks across different quality axes.

## Objectives
- Build a resilient engineering foundation.
- Maximize VRAM usage efficiency.
- Establish clean architectural boundaries.
- Fully automate evaluation and deployment procedures.
