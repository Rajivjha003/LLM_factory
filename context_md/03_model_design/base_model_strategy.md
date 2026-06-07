# Base Model Strategy

## Principle
Choose the smallest model that can solve the task after specialization.

## Default Progression
1. Validate pipeline on 1B/1.5B.
2. Iterate on 3B.
3. Train serious local model at 7B/8B.
4. Try 14B only after pipeline is stable.

## Selection Checklist
- License checked
- Fits hardware
- Unsloth compatible
- vLLM compatible
- GGUF convertible
- Strong code/SQL ability
- Good chat template
- Active community

## Avoid
- Huge models that cannot be iterated locally.
- Obscure models with poor tooling.
- Models with unclear license.
