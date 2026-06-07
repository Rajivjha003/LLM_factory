# Hyperparameter Plan

## First QLoRA Defaults
- LoRA rank: 16
- Alpha: 32
- Dropout: 0.05
- LR: 2e-4 for SFT starting point
- Batch: 1
- Grad accumulation: 8-32
- Max seq length: 2048
- Epochs: 1-3 depending dataset

## Tuning Order
1. Data quality
2. Learning rate
3. Epochs
4. LoRA rank
5. Sequence length
6. Batch/effective batch

## Rule
Do not tune five variables at once.
