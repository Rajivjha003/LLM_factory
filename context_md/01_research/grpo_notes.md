# GRPO Notes

## Purpose
Use GRPO or verifier-based reinforcement learning for tasks where reward can be checked automatically.

## Best Use Cases
- SQL generation correctness
- Python/code unit tests
- JSON/schema validity
- Math/verifiable reasoning
- Tool call correctness
- Data reconciliation workflows

## Reward Design
Reward should be specific, testable, and hard to game.

Example reward components:
- Valid syntax: +1
- Correct schema use: +1
- Read-only SQL: +1
- Correct result shape: +1
- Hallucinated column: -1
- Unsafe mutation: -2

## Policy
Use SFT first, DPO second, GRPO third. Do not jump straight to GRPO without stable behavior and evals.
