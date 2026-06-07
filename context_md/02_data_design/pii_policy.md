# PII Policy

## Do Not Train On
- Passwords
- API keys
- Tokens
- Personal phone numbers
- Email addresses unless public/allowed
- Addresses
- Private customer data
- Private client records

## Allowed After Redaction
- Schemas
- Table names where permitted
- Synthetic rows
- Aggregated metrics
- Anonymized examples

## Redaction Pattern
Replace sensitive values with stable placeholders:
- `<EMAIL>`
- `<PHONE>`
- `<TOKEN>`
- `<CLIENT>`
- `<USER_ID>`
- `<ORDER_ID>`

## Principle
Never put secrets or private production data into SFT/preference/GRPO training files.
