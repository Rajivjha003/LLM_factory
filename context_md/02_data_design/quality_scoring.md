# Quality Scoring

## Scale
1 = unusable/noisy
2 = weak/partial
3 = acceptable
4 = strong
5 = gold-standard

## Gold-Standard Example Criteria
- Correct answer
- Clear reasoning summary
- Domain-specific
- Uses exact table/column context when available
- Includes validation step
- Safe and non-destructive
- Concise but complete

## Dataset Use Rules
- SFT v1: use only score 4-5.
- Preference data: chosen should be 4-5, rejected can be 1-3.
- Eval data: must be manually reviewed.
