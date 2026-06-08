#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"
BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
SFT_ADAPTER="artifacts/adapters/qwen_1_5b_sft_v2_failure_driven"
MERGED_MODEL="artifacts/merged/qwen_1_5b_sft_v2_merged"
DPO_ADAPTER="artifacts/adapters/qwen_1_5b_dpo_v2_human"

echo "== Phase 6B: Human-Curated DPO v2 =="

python scripts/parse_human_dpo_v2_curation_pack.py \
  --input-md reports/dpo_curation/dpo_v2_curation_pack.md \
  --output-jsonl data/preferences/merchmix_dpo_v2_human.jsonl \
  --min-pairs 40

python scripts/validate_dpo_v2_dataset.py \
  --path data/preferences/merchmix_dpo_v2_human.jsonl \
  --min-count 40

python scripts/audit_dpo_v2_quality.py \
  --path data/preferences/merchmix_dpo_v2_human.jsonl \
  --output-md reports/dpo_curation/dpo_v2_quality_report.md

python scripts/merge_lora_adapter.py \
  --base-model "$BASE_MODEL" \
  --adapter "$SFT_ADAPTER" \
  --output-model "$MERGED_MODEL"

python scripts/run_dpo_lora_v2.py \
  --config configs/training/dpo_qwen_1_5b_v2_human.yaml

python scripts/run_adapter_eval_v3.py \
  --base-model "$MERGED_MODEL" \
  --adapter "$DPO_ADAPTER" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.metadata.json

python scripts/compare_champion_vs_candidate_judge_v3.py \
  --champion reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
  --candidate reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.jsonl \
  --candidate-name qwen_1_5b_dpo_v2_human \
  --output-md reports/model_matrix/dpo_v2_promotion_report.md \
  --output-json reports/model_matrix/dpo_v2_promotion_report.json

echo "== Phase 6B complete =="
