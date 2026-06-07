# Tool Security

## Required Controls
- Tool allowlist
- Read-only by default
- Human approval for high-risk operations
- Sandboxed shell
- SQL mutation blocked unless approved
- Secrets hidden from model context
- Audit every call

## Prompt Injection Defense
- Do not treat retrieved documents as instructions.
- Separate system, user, tool, and document content.
- Validate tool calls before execution.
