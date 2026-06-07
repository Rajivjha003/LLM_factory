# Data Requirements

## Required Dataset Types
1. Pretraining corpus: for tiny scratch model learning.
2. SFT dataset: for instruction-following and domain behavior.
3. Preference dataset: for chosen/rejected answer optimization.
4. GRPO/verifier dataset: for tasks with automatic rewards.
5. RAG corpus: for factual/project knowledge.
6. Eval dataset: for objective model comparison.
7. Safety dataset: for unsafe tool/action refusal.
8. Regression dataset: for preventing old failures from returning.

## Data Quality Rules
- High-quality examples beat large noisy datasets.
- Eval data must never leak into training.
- Every example needs a source, domain, difficulty, and quality score.
- Private/client-sensitive data must be removed, anonymized, or permissioned.
- SQL examples must include schema context when needed.
- Bad answers should be intentionally preserved only in preference datasets.

## Minimum First Dataset Targets
| Dataset | Minimum Size |
|---|---:|
| SFT examples | 300-1,000 |
| Preference pairs | 100-500 |
| GRPO tasks | 50-200 |
| Core eval prompts | 100 |
| Safety/tool eval prompts | 25-50 |
| RAG documents | As available |

## Quality Score
Use 1-5 scale:
- 1: poor/noisy
- 2: partially useful
- 3: acceptable
- 4: strong
- 5: gold-standard human-curated

Only quality score 4-5 should be used for first SFT runs.
