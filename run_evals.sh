#!/bin/bash
set -euo pipefail
source .venv/bin/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

python scripts/run_adapter_eval_v3.py \
    --base-model artifacts/merged/qwen_1_5b_sft_v2_merged \
    --adapter artifacts/adapters/qwen_1_5b_dpo_v1 \
    --eval-dir data/eval_v3 \
    --output-jsonl reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
    --output-md reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.md \
    --metadata-json reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.metadata.json

python scripts/build_judge_v3_model_matrix.py \
    --outputs reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
    --output-md reports/model_matrix/model_matrix_phase6_dpo_v1.md
