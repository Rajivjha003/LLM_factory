# Planner-Executor-Verifier

## Planner
Breaks user goal into steps.

## Executor
Runs approved tool calls or generation steps.

## Verifier
Checks output correctness, safety, and format.

## Retry Loop
If verifier fails, feed error back and retry within limit.

## Human Gate
High-risk actions require approval.
