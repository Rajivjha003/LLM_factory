#!/usr/bin/env bash
set -euo pipefail

BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
ADAPTER="artifacts/adapters/qwen_1_5b_sft_v2_failure_driven"

echo "== Phase 4.5 Truth Audit =="

python scripts/build_holdout_eval_v3.py --output-dir data/eval_v3

python scripts/validate_eval_data.py \
  --eval-dir data/eval_v3 \
  --expected-count 50

python scripts/build_dataset_hash_manifest.py \
  --dataset-dir data/eval_v3 \
  --output reports/truth_audit/eval_v3_hash_manifest.json

python scripts/check_eval_prompt_uniqueness.py \
  --eval-dir data/eval_v3 \
  --output-md reports/truth_audit/eval_v3_prompt_uniqueness.md

python scripts/check_train_eval_leakage_full.py \
  --sft data/sft/merchmix_sft_v3.jsonl \
  --eval-dir data/eval_v3 \
  --output-json reports/truth_audit/sft_v3_eval_v3_leakage_audit.json \
  --lexical-output reports/truth_audit/sft_v3_eval_v3_lexical_overlap.md \
  --semantic-output reports/truth_audit/sft_v3_eval_v3_semantic_overlap.md

python scripts/run_adapter_eval_v2.py \
  --base-model "$BASE_MODEL" \
  --adapter "$ADAPTER" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.metadata.json

python scripts/audit_eval_report.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v2_eval_v3_report_audit.json

python scripts/audit_judge_v2_thresholds.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
  --output-md reports/truth_audit/qwen_1_5b_sft_v2_eval_v3_judge_threshold_audit.md

python scripts/bootstrap_eval_confidence.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v2_eval_v3_confidence.json

python scripts/sample_human_review_pack.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
  --output-md reports/truth_audit/qwen_1_5b_sft_v2_eval_v3_human_review_pack.md \
  --sample-size 20

PYTHONPATH=. pytest tests/test_eval_v3_integrity.py tests/test_report_audit.py

echo "== Truth audit completed =="
