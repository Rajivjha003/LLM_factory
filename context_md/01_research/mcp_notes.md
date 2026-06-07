# MCP Notes

## Purpose
MCP-style tool contracts allow models/agents to interact with external tools in a standardized way.

## What MCP Provides
- Tool discovery
- Tool schemas
- Contract-based execution
- Better separation between model and tool implementation

## What MCP Does Not Provide Alone
- Security
- Correctness
- Permissioning
- Sandboxing
- Human approval

## Required Architecture
MCP must sit behind:
- Tool allowlist
- Permission layer
- Human approval gates
- Audit log
- Sandboxed execution
- Verifier loop

## Principle
MCP is an integration protocol, not a trust boundary.
