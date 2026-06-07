# Self-Correction Loop

## Flow
Attempt -> Tool/Error Result -> Diagnose -> Correct -> Retry -> Final

## Use Cases
- SQL syntax error
- Missing column
- Failed API call
- Invalid JSON
- Tool timeout

## Limits
- Max retries per task
- Escalate to user/human when repeated failure occurs
