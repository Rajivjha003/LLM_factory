# Evaluation Framework

## Layers
1. Unit eval: parse validity, JSON validity, SQL read-only.
2. Task eval: does answer solve the problem?
3. Domain eval: is retail/data logic correct?
4. RAG eval: is answer grounded?
5. Safety eval: does it avoid dangerous actions?
6. Regression eval: did previous behavior break?
7. Latency eval: can it run on hardware?

## Evaluation Rule
Every model version must have an eval report before promotion.
