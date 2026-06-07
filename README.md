# LLM Ops

An advanced platform for operationalizing Large Language Models (LLMs). This project handles end-to-end LLM lifecycles, from fine-tuning (SFT, DPO, GRPO) and quantization to high-performance serving and automated evaluations.

## Project Structure
- `src/llm_ops/`: Core engineering foundation, including configuration, exceptions, logging, and utilities.
- `scripts/`: Utilities for system health checks and routine operations.
- `docs/`: Comprehensive project documentation, requirements, and roadmaps.
- `tests/`: Automated tests ensuring platform reliability.

## Setup Instructions
1. Ensure your environment uses Python 3.10+ (matching `.python-version`).
2. Install dependencies (e.g., using `uv` or `pip`).
3. Run health checks:
   ```bash
   python scripts/check_train_env.py
   python scripts/check_vllm_env.py
   ```
4. Check the `docs/` folder for deeper architectural and design details.
