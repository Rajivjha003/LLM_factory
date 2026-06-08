# Judge v3 Human Calibration Report

- Total labeled: 25
- Judge agreement rows: 25
- Judge agreement rate: 100.0%
- Recommendation: `judge_v3_ready`

## Human Correctness

| Label | Count |
|---|---:|
| yes | 25 |

## Primary Issues

| Issue | Count |
|---|---:|
| correct | 25 |

## Decision Rules

- If agreement >= 80% on at least 20 labels: Judge v3 can be used as promotion gate.
- If agreement < 80%: inspect disagreements and calibrate Judge v3.
- If false positives are safety-related: SQL verifier must dominate promotion decisions.