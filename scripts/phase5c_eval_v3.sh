#!/usr/bin/env bash
set -euo pipefail

BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"

ADAPTER_V2="artifacts/adapters/qwen_1_5b_sft_v2_failure_driven"
ADAPTER_V4B="artifacts/adapters/qwen_1_5b_sft_v4b_realworld"

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

echo "Running Judge v3 on SFT v2 (Champion)..."
python scripts/run_adapter_eval_v3.py \
  --base-model "$BASE_MODEL" \
  --adapter "$ADAPTER_V2" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.metadata.json

echo "Running Judge v3 on SFT v4b..."
python scripts/run_adapter_eval_v3.py \
  --base-model "$BASE_MODEL" \
  --adapter "$ADAPTER_V4B" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v3.metadata.json

echo "Evaluation Complete."
