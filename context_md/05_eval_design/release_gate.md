# Release Gate

A model is released only if:

- Base model benchmark exists.
- Fine-tuned benchmark exists.
- Domain score improves.
- Safety score does not regress.
- Latency is acceptable.
- VRAM fits hardware.
- Quantized artifact tested.
- Model card exists.
- Dataset version recorded.
- Rollback version available.

## Release Decision
- Promote
- Hold
- Reject
- Needs more eval
