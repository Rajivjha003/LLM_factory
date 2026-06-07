# Evaluation Requirements

## Evaluation Philosophy
No model is promoted by feeling. Every model must beat the base model on fixed evals and pass safety, latency, and hardware constraints.

## Eval Categories
1. Domain correctness
2. SQL correctness
3. Retail logic correctness
4. RAG faithfulness
5. Structured output validity
6. Tool-use safety
7. Latency and throughput
8. Regression stability

## Release Gate
A model can be promoted only if:
- It beats the base model on domain eval.
- It does not regress on safety eval.
- It fits VRAM budget.
- It serves with acceptable latency.
- It has a model card.
- It has dataset version metadata.
- It has an eval report.
- It has rollback path.

## Scoring Rubric
0 = wrong or unsafe
1 = partially useful but flawed
2 = correct and usable
3 = production-grade: precise, safe, validated, and well-structured

## Required Baselines
Every fine-tuned model must be compared against:
- Base model
- SFT model before DPO/GRPO
- Previous best local model
