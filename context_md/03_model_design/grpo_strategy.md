# GRPO Strategy

## Purpose
Train reasoning behavior using automatic reward/verifier signals.

## Best Domains
- SQL generation
- Code generation
- Tool call correctness
- JSON validity
- Data reconciliation

## Reward Function Requirements
- Deterministic where possible
- Simple first
- Penalize unsafe actions
- Detect hallucinated schemas
- Detect invalid output format

## Training Policy
Do not expose long chain-of-thought by default in production. Train structured reasoning internally and output concise reasoning summaries.
