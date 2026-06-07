# Security Requirements

## Core Principle
MCP and tool calling are integration protocols, not security boundaries. Every tool must be sandboxed, permissioned, logged, and limited.

## Tool Risk Levels
| Tool | Risk | Control |
|---|---|---|
| Calculator | Low | Allow |
| File read | Medium | Path allowlist |
| SQL SELECT | Medium | Read-only DB user |
| SQL INSERT/UPDATE/DELETE | High | Human approval |
| Shell command | High | Sandbox only |
| Web browsing | Medium | Domain policy |
| Email/send action | High | Human approval |
| Cloud deployment | High | Human approval |

## Required Controls
- Tool allowlist
- Human approval for high-risk actions
- Read-only credentials by default
- SQL mutation disabled by default
- Shell commands sandboxed
- Path allowlists for file operations
- Audit logs for every tool call
- Prompt injection checks for RAG/tool content
- Secrets never placed in training data

## Unsafe Actions
The agent must not autonomously:
- Delete production data
- Modify cloud resources
- Send emails/messages
- Run arbitrary shell commands
- Exfiltrate credentials
- Execute unreviewed SQL mutations
