# QLoRA Strategy

## Purpose
Fine-tune larger models within 16 GB VRAM.

## Default Config Direction
- Load base in 4-bit
- Quant type: NF4
- Compute dtype: bf16 or fp16 depending support
- LoRA rank: start 16
- LoRA alpha: 32
- LoRA dropout: 0.05
- Batch size: 1 first
- Gradient accumulation: 8-32
- Max sequence length: start 2048
- Gradient checkpointing: enabled

## OOM Fallback Order
1. Reduce sequence length.
2. Reduce batch size to 1.
3. Increase gradient accumulation instead.
4. Reduce LoRA rank.
5. Use smaller base model.
