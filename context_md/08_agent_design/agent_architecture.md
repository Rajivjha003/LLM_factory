# Agent Architecture

## Flow
User Request -> Intent Classifier -> Planner -> Tool Router -> Tool/MCP -> Verifier -> Self-Correction -> Final Answer

## Components
- Planner
- Tool selector
- Tool permission layer
- MCP client/server contracts
- Execution sandbox
- Verifier
- Retry policy
- Memory store
- Audit log
- Human approval gate
