#!/usr/bin/env bash
set -euo pipefail

BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
SFT_ADAPTER="artifacts/adapters/qwen_1_5b_sft_v2_failure_driven"
MERGED_MODEL="artifacts/merged/qwen_1_5b_sft_v2_merged"
DPO_ADAPTER="artifacts/adapters/qwen_1_5b_dpo_v1"

echo "== Phase 6 DPO End-to-End =="

python scripts/parse_human_review_pack.py \
  --input reports/truth_audit/human_review_pack.md \
  --output data/human_review/human_review_labels_v1.jsonl

python scripts/calibrate_judge_v3_with_human.py \
  --human-labels data/human_review/human_review_labels_v1.jsonl \
  --output-md reports/truth_audit/judge_v3_human_calibration.md \
  --output-json reports/truth_audit/judge_v3_human_calibration.json

python scripts/build_dpo_dataset_v1.py \
  --judge-v3-results reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
  --human-labels data/human_review/human_review_labels_v1.jsonl \
  --output data/preferences/merchmix_dpo_v1.jsonl \
  --target-count 80

python scripts/validate_dpo_dataset.py \
  --path data/preferences/merchmix_dpo_v1.jsonl \
  --min-count 20

python scripts/merge_lora_adapter.py \
  --base-model "$BASE_MODEL" \
  --adapter "$SFT_ADAPTER" \
  --output-model "$MERGED_MODEL"

python scripts/run_dpo_lora.py \
  --config configs/training/dpo_qwen_1_5b_v1.yaml

python scripts/run_adapter_eval_v3.py \
  --base-model "$MERGED_MODEL" \
  --adapter "$DPO_ADAPTER" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.metadata.json

python scripts/build_judge_v3_model_matrix.py \
  --outputs \
    reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
    reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
  --output-md reports/model_matrix/model_matrix_phase6_dpo_v1.md

echo "== Phase 6 DPO complete =="
