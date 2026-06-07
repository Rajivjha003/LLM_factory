# Hardware Constraints

## Machine
- Device: Alienware
- CPU: Intel Core i9-14900HX
- RAM: 64 GB
- GPU: NVIDIA GeForce RTX 4090 Laptop
- VRAM: 16 GB
- Storage free: approximately 1.63 TB
- OS: Windows 11 Home

## Operating System Strategy
Use WSL2 Ubuntu 24.04 for all serious LLM work. Avoid native Windows Python for CUDA-heavy training.

## Python Version
Use Python 3.11 as the default project version.

## Local Training Envelope
| Task | Recommended Limit |
|---|---|
| Scratch pretraining | 30M-300M parameters |
| Fast fine-tuning | 0.5B-3B models |
| Main local QLoRA | 7B-8B models |
| Stretch QLoRA | 14B with compromises |
| Full fine-tune 7B+ | Not local priority |
| Context length training | Start 2k, later 4k |
| Physical batch size | 1-2 |
| Gradient accumulation | 8-32 |

## Memory Rules
- Prefer QLoRA over full fine-tuning.
- Prefer 3B for fast experiments.
- Use 7B/8B for serious local quality.
- Use GGUF Q4_K_M/Q5_K_M for local inference.
- Use vLLM for API serving when compatible.
- Use cloud only when model size or throughput requires it.

## OOM Prevention
- Start with short context.
- Use gradient checkpointing.
- Use batch size 1 first.
- Increase sequence length only after stable runs.
- Keep eval batches small.
- Monitor VRAM continuously.
