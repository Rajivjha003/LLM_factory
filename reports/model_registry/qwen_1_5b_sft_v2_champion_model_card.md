# Champion Model Card — Qwen 1.5B SFT v2

Created UTC: `2026-06-08T06:17:26.741859+00:00`
Git commit: `3d8985ac28064960f1063842486bb8dcb496c856`

## Champion

- Base model: `/home/rajiv/models/base/qwen2_5_1_5b_instruct`
- Adapter: `artifacts/adapters/qwen_1_5b_sft_v2_failure_driven`
- Merged model: `artifacts/merged/qwen_1_5b_sft_v2_merged`
- Evaluation set: `data/eval_v3`
- Judge: Judge v3 + SQL verifier

## Verified Champion Metrics

- Judge v3 pass: 44/50 = 88%
- SQL verifier pass: 44/50 = 88%
- Strict Judge v2 pass: 17/50 = 34%

## Promotion History

- SFT v4: rejected.
- SFT v4b: rejected.
- Qwen 3B QLoRA v1: rejected.
- DPO v1: rejected.
- DPO v2: rejected/tied, not promoted.

## Intended Use

Merchmix retail/data-engineering assistant for:

- BigQuery debugging
- SQL generation and validation
- Postgres vs BigQuery reconciliation
- WSSI / CSOH / retail metric reasoning
- Pipeline debugging
- Safe read-only data diagnostics

## Safety Rules

- Must prefer read-only SQL.
- Must not place destructive SQL inside executable SQL blocks.
- Must use preview/backup/validation framing for production changes.
- Must explain query interpretation and next checks.

## Limitations

- Not a production autonomous database agent.
- SQL verifier is semantic/static, not a full BigQuery dry-run verifier yet.
- Human review is still required for high-risk production changes.