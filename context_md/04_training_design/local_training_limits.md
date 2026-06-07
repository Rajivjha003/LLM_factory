# Local Training Limits

## Defaults
- Python: 3.11
- OS: WSL2 Ubuntu 24.04
- GPU: RTX 4090 Laptop 16 GB
- Main model size: 7B-8B QLoRA
- Fast iteration size: 1B-3B

## Sequence Length
Start 2048. Move to 4096 only after stable memory behavior.

## Batch
Start physical batch size 1.

## Gradient Accumulation
Use 8-32 depending target effective batch size.

## Warning
Do not start with max context, 14B model, and high LoRA rank at the same time.
