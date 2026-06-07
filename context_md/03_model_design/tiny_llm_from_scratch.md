# Tiny LLM From Scratch

## Purpose
Learn architecture, not production quality.

## Recommended Spec
- Params: 30M-125M first
- Context: 512-1024
- Vocab: 16k-32k
- Architecture: decoder-only Transformer
- Attention: causal self-attention
- Position: RoPE if implemented
- Objective: next-token prediction

## Success Criteria
- Training loop runs on GPU.
- Loss decreases.
- Checkpoint saves and reloads.
- Model can generate coherent-ish text.
- Perplexity can be measured.
