# Adapter Merge Strategy

## Purpose
Merge LoRA adapters into base model when needed for deployment or quantization.

## Policy
- Keep adapter separately for reproducibility.
- Merge only after eval passes.
- Save merged model as new artifact.
- Never delete base/adapters.
