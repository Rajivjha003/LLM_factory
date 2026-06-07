# SFT Strategy

## Purpose
Teach response format, domain style, and assistant behavior.

## Method
Use Unsloth QLoRA where supported, with TRL SFTTrainer or equivalent.

## First Target
1B-3B model for fast iteration.

## Main Target
7B-8B model with QLoRA.

## Data
Use only quality score 4-5 examples.

## Output Behavior
The model should produce:
- Direct diagnosis
- Exact query/code/checklist where useful
- Short reasoning summary
- Clear validation step
- Safe final recommendation
