# Memory Budget

## VRAM Budget Strategy
Reserve VRAM for:
- Model weights
- LoRA adapters
- Activations
- Gradients
- Optimizer states
- KV/cache during eval

## Memory Reduction Tools
- 4-bit QLoRA
- Gradient checkpointing
- Lower sequence length
- Lower batch size
- Smaller LoRA rank
- Smaller model
- FlashAttention where available

## OOM Debug Checklist
1. Confirm only one training process is running.
2. Reduce max sequence length.
3. Reduce batch size.
4. Enable gradient checkpointing.
5. Reduce LoRA rank.
6. Restart kernel/session to clear VRAM.
7. Try smaller model.
