# Pruning Policy

## Rule
Do not prune early.

## Preferred Order
1. Quantization
2. Better serving engine
3. Distillation
4. Pruning

## Why
Pruning can damage model quality silently unless evals are strong.
