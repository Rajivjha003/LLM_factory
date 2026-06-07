# Retraining Policy

## Retrain When
- Enough high-quality new examples exist.
- Repeated failure class appears.
- Base model upgrade is chosen.
- Eval set changes materially.

## Do Not Retrain For
- One-off random failure
- Bad prompt only
- Missing RAG document that should be retrieved instead
