# Phase 6 Package — Human-Calibrated Judge v3 + DPO v1

Current champion:

- Base: Qwen2.5-1.5B-Instruct
- Adapter: `artifacts/adapters/qwen_1_5b_sft_v2_failure_driven`
- Frozen benchmark: `data/eval_v3`
- Promotion gate: Judge v3 + SQL verifier + human calibration

Run order:

```bash
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
  --base-model /home/rajiv/models/base/qwen2_5_1_5b_instruct \
  --adapter artifacts/adapters/qwen_1_5b_sft_v2_failure_driven \
  --output-model artifacts/merged/qwen_1_5b_sft_v2_merged

python scripts/run_dpo_lora.py \
  --config configs/training/dpo_qwen_1_5b_v1.yaml

python scripts/run_adapter_eval_v3.py \
  --base-model artifacts/merged/qwen_1_5b_sft_v2_merged \
  --adapter artifacts/adapters/qwen_1_5b_dpo_v1 \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.metadata.json

python scripts/build_judge_v3_model_matrix.py \
  --outputs \
    reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
    reports/eval_reports/qwen_1_5b_dpo_v1_eval_v3_judge_v3.jsonl \
  --output-md reports/model_matrix/model_matrix_phase6_dpo_v1.md
```

Promotion rule:

- DPO must beat SFT v2 champion on Judge v3 pass rate or SQL verifier pass rate.
- It must not regress SQL safety.
- If human-reviewed disagreement is high, do not promote DPO.
