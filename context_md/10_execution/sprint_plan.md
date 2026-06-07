# Sprint Plan

## Sprint 1: Requirement Lock
- Complete requirement docs.
- Lock hardware assumptions.
- Lock first use cases.
- Define model/eval strategy.

## Sprint 2: Environment Validation
- WSL2 Ubuntu.
- Python 3.11.
- uv.
- CUDA/PyTorch check.
- Run basic inference.

## Sprint 3: Data Foundation
- Create first SFT schema.
- Create 100-300 examples.
- Create 50 eval prompts.
- Add quality scoring.

## Sprint 4: First SFT
- Fine-tune 1B/3B.
- Evaluate.
- Fix data.

## Sprint 5: Main 7B/8B QLoRA
- Fine-tune main local model.
- Evaluate against base.

## Sprint 6: DPO and GRPO Prototype
- Build preference pairs.
- Build verifier tasks.
- Run small alignment experiments.

## Sprint 7: Quantization and Serving
- Merge adapter.
- GGUF quantization.
- llama.cpp serving.
- vLLM serving.

## Sprint 8: Agent + LLMOps
- Tool router.
- MCP contracts.
- Eval gate.
- Monitoring and feedback.
