# DPO Strategy

## Purpose
Make the model prefer better answers without full RLHF complexity.

## When To Use
After SFT produces stable behavior.

## Dataset
Chosen/rejected pairs.

## Good Preferences
Chosen answer should be:
- More correct
- More specific
- Safer
- Better structured
- More production-ready

## Bad Preferences
Rejected answer may be:
- Vague
- Unsafe
- Hallucinated
- Too verbose
- Missing validation

## Policy
Run DPO before GRPO unless the task is purely verifier-based.
