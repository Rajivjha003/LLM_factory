#!/usr/bin/env bash
set -euo pipefail

BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
ADAPTER_V4B="artifacts/adapters/qwen_1_5b_sft_v4b_realworld"

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

echo "5. Evaluate SFT v4b on frozen eval_v3"
python scripts/run_adapter_eval_v2.py \
  --base-model "$BASE_MODEL" \
  --adapter "$ADAPTER_V4B" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.metadata.json

echo "6. Audit report math"
python scripts/audit_eval_report.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v4b_eval_v3_report_audit.json

echo "7. Bootstrap confidence"
python scripts/bootstrap_eval_confidence.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v4b_eval_v3_confidence.json

echo "8. Judge threshold audit"
python scripts/audit_judge_v2_thresholds.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-md reports/truth_audit/qwen_1_5b_sft_v4b_eval_v3_threshold_audit.md

echo "9. Failure taxonomy"
python scripts/build_judge_v2_failure_taxonomy.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-md reports/failure_taxonomy/qwen_1_5b_sft_v4b_eval_v3_taxonomy.md

echo "10. Model matrix update"
python scripts/build_model_matrix_v2.py \
  --outputs \
    reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
    reports/eval_reports/qwen_3b_qlora_v1_from_sft_v3_eval_v3_judge_v2.jsonl \
    reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
    reports/eval_reports/qwen_1_5b_sft_v4b_eval_v3_judge_v2.jsonl \
  --output-md reports/model_matrix/model_matrix_phase5b_eval_v3.md

echo "== Phase 5B Evaluation completed =="
