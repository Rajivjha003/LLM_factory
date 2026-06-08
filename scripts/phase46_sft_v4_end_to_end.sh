#!/usr/bin/env bash
set -euo pipefail

BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
ADAPTER_V4="artifacts/adapters/qwen_1_5b_sft_v4_realworld_rubric"

echo "== Phase 4.6: SFT v4 End-to-End =="

echo "1. Generate rubric additions"
python scripts/generate_rubric_sft_v4_additions.py \
  --output data/sft/generated/rubric_sft_v4_additions.jsonl \
  --count 300 \
  --seed 42

echo "2. Ensure real-world additions file exists"
touch data/sft/real_world_clean/real_world_sft_v4_additions.jsonl

echo "3. Build SFT v4"
python scripts/build_sft_v4.py \
  --base-sft data/sft/merchmix_sft_v3.jsonl \
  --rubric-additions data/sft/generated/rubric_sft_v4_additions.jsonl \
  --real-additions data/sft/real_world_clean/real_world_sft_v4_additions.jsonl \
  --output data/sft/merchmix_sft_v4.jsonl \
  --target-count 900

echo "4. Validate SFT schema"
python scripts/validate_sft_data.py \
  --path data/sft/merchmix_sft_v4.jsonl

echo "5. Validate SFT quality"
python scripts/validate_sft_v4_quality.py \
  --sft data/sft/merchmix_sft_v4.jsonl \
  --output-md reports/sft_quality/sft_v4_quality_report.md \
  --min-count 800

echo "6. Check lexical overlap with eval_v3"
python scripts/check_sft_eval_overlap_strict.py \
  --sft data/sft/merchmix_sft_v4.jsonl \
  --eval-dir data/eval_v3 \
  --output reports/truth_audit/sft_v4_eval_v3_lexical_overlap.md \
  --fail-threshold 0.80

echo "7. Check semantic overlap with eval_v3"
python scripts/check_semantic_overlap.py \
  --sft data/sft/merchmix_sft_v4.jsonl \
  --eval-dir data/eval_v3 \
  --output-md reports/truth_audit/sft_v4_eval_v3_semantic_overlap.md \
  --fail-threshold 0.88

echo "8. Train Qwen 1.5B SFT v4"
python scripts/run_sft_lora.py \
  --config configs/training/sft_qwen_1_5b_lora_v4.yaml

echo "9. Evaluate SFT v4 on frozen eval_v3"
python scripts/run_adapter_eval_v2.py \
  --base-model "$BASE_MODEL" \
  --adapter "$ADAPTER_V4" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.metadata.json

echo "10. Audit report math"
python scripts/audit_eval_report.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v4_eval_v3_report_audit.json

echo "11. Bootstrap confidence"
python scripts/bootstrap_eval_confidence.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-json reports/truth_audit/qwen_1_5b_sft_v4_eval_v3_confidence.json

echo "12. Judge threshold audit"
python scripts/audit_judge_v2_thresholds.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-md reports/truth_audit/qwen_1_5b_sft_v4_eval_v3_threshold_audit.md

echo "13. Failure taxonomy"
python scripts/build_judge_v2_failure_taxonomy.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-md reports/failure_taxonomy/qwen_1_5b_sft_v4_eval_v3_taxonomy.md

echo "14. Model matrix"
python scripts/build_model_matrix_v2.py \
  --outputs \
    reports/eval_reports/qwen_1_5b_sft_v1_eval_v3_judge_v2.jsonl \
    reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v2.jsonl \
    reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-md reports/model_matrix/model_matrix_phase46_eval_v3.md

echo "15. Human review pack"
python scripts/sample_human_review_pack.py \
  --eval-jsonl reports/eval_reports/qwen_1_5b_sft_v4_eval_v3_judge_v2.jsonl \
  --output-md reports/truth_audit/qwen_1_5b_sft_v4_eval_v3_human_review_pack.md \
  --sample-size 20

echo "16. Tests"
PYTHONPATH=src pytest tests/test_eval_v3_integrity.py tests/test_report_audit.py tests/test_judge_v2.py tests/test_sft_v4_quality.py

echo "== Phase 4.6 completed =="
