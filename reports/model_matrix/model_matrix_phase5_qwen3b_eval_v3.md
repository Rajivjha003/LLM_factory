# Phase 5 Model Matrix

| Model | Eval | Pass Rate | Score Rate | Status |
|---|---:|---:|---:|---|
| qwen_1_5b_sft_v2_eval_v3 | eval_v3 | 34.0% | 92.7% | Current champion before Phase 5 |
| qwen_3b_qlora_v1_from_sft_v3 | eval_v3 | 2.0% | 36.4% | REJECT_OR_HOLD: keep 1.5B champion; data/judge/verifier is bottleneck. |

## Decision

REJECT_OR_HOLD: keep 1.5B champion; data/judge/verifier is bottleneck.

## Gates

- Minimum candidate: 38.0%
- Strong promotion: 45.0%
- Excellent: 55.0%