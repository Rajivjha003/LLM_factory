# Training Pipeline

## Pipeline
1. Select base model.
2. Select dataset version.
3. Validate dataset schema.
4. Run baseline eval on base model.
5. Train SFT/QLoRA.
6. Evaluate.
7. Run DPO if preference data exists.
8. Evaluate.
9. Run GRPO if verifier tasks exist.
10. Evaluate.
11. Merge adapter if needed.
12. Quantize.
13. Serve.
14. Monitor and collect feedback.

## Rule
Each stage must produce an artifact and an eval report before moving to the next stage.
