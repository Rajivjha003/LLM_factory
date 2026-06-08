# Phase 6B — Human-Curated DPO v2

## Why this phase exists

DPO v1 failed promotion:

- SFT v2 Champion:
  - Judge v3: 44/50 = 88%
  - SQL verifier: 44/50 = 88%

- DPO v1:
  - Judge v3: 41/50 = 82%
  - SQL verifier: 40/50 = 80%

Conclusion:

DPO itself is not rejected. DPO v1 failed because the preference data was too bootstrapped and not human-curated enough.

## Phase 6B Objective

Build a higher-quality DPO v2 dataset from human-reviewed examples, train conservatively, and only promote if it beats the SFT v2 champion.

## Core rule

Do not train DPO v2 until you have at least 40 high-quality human-curated preference pairs.

Recommended target:

- Minimum: 40 pairs
- Good: 80 pairs
- Strong: 120 pairs

## Run order

```bash
cd ~/LLM_Ops
source .venv/bin/activate

# 1. Build curation pack from model failures / human-review-needed rows
python scripts/build_human_dpo_v2_curation_pack.py \
  --judge-v3-results reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
  --output-md reports/dpo_curation/dpo_v2_curation_pack.md \
  --max-items 80

# 2. Fill chosen answers manually in the markdown
# Edit reports/dpo_curation/dpo_v2_curation_pack.md

# 3. Parse curated markdown into JSONL
python scripts/parse_human_dpo_v2_curation_pack.py \
  --input-md reports/dpo_curation/dpo_v2_curation_pack.md \
  --output-jsonl data/preferences/merchmix_dpo_v2_human.jsonl \
  --min-pairs 40

# 4. Validate quality
python scripts/validate_dpo_v2_dataset.py \
  --path data/preferences/merchmix_dpo_v2_human.jsonl \
  --min-count 40

# 5. Audit quality report
python scripts/audit_dpo_v2_quality.py \
  --path data/preferences/merchmix_dpo_v2_human.jsonl \
  --output-md reports/dpo_curation/dpo_v2_quality_report.md

# 6. Merge SFT champion if not already done
python scripts/merge_lora_adapter.py \
  --base-model /home/rajiv/models/base/qwen2_5_1_5b_instruct \
  --adapter artifacts/adapters/qwen_1_5b_sft_v2_failure_driven \
  --output-model artifacts/merged/qwen_1_5b_sft_v2_merged

# 7. Train DPO v2
python scripts/run_dpo_lora_v2.py \
  --config configs/training/dpo_qwen_1_5b_v2_human.yaml

# 8. Evaluate DPO v2 with Judge v3
python scripts/run_adapter_eval_v3.py \
  --base-model artifacts/merged/qwen_1_5b_sft_v2_merged \
  --adapter artifacts/adapters/qwen_1_5b_dpo_v2_human \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.metadata.json

# 9. Compare to champion
python scripts/compare_champion_vs_candidate_judge_v3.py \
  --champion reports/eval_reports/qwen_1_5b_sft_v2_eval_v3_judge_v3.jsonl \
  --candidate reports/eval_reports/qwen_1_5b_dpo_v2_eval_v3_judge_v3.jsonl \
  --candidate-name qwen_1_5b_dpo_v2_human \
  --output-md reports/model_matrix/dpo_v2_promotion_report.md \
  --output-json reports/model_matrix/dpo_v2_promotion_report.json

# 10. End-to-end runner after curation is complete
./scripts/phase6b_dpo_v2_end_to_end.sh
```

## Promotion rule

DPO v2 only becomes champion if:

1. Judge v3 pass count > 44/50 OR SQL verifier pass count > 44/50
2. Safety does not regress
3. Human-review-required count does not increase materially
4. Report audit passes
5. Manual spot check passes

If DPO v2 does not beat SFT v2, reject it and proceed to Phase 7 with SFT v2 champion.
