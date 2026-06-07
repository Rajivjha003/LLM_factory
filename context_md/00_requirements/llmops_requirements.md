# LLMOps Requirements

## Required Capabilities
- Dataset versioning
- Experiment tracking
- Model registry
- Eval report generation
- Artifact storage
- Serving configuration
- Monitoring and logging
- Feedback collection
- Retraining policy
- Rollback policy

## Required Metadata Per Run
- Model name and version
- Base model hash/revision
- Dataset version
- Training method: SFT, QLoRA, DPO, GRPO
- Hyperparameters
- Hardware profile
- Training duration
- Peak VRAM
- Eval results
- Known failures
- Release decision

## Lifecycle
Data -> Train -> Eval -> Register -> Quantize -> Serve -> Monitor -> Feedback -> Retrain

## Promotion Policy
No model moves to serving unless it passes release gate in `05_eval_design/release_gate.md`.
