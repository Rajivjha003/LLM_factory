# Deployment Runbook

## Steps
1. Select model artifact.
2. Confirm eval pass.
3. Confirm quantized artifact exists.
4. Start backend: llama.cpp or vLLM.
5. Start FastAPI gateway.
6. Run health check.
7. Run smoke test.
8. Enable logging.
9. Collect feedback.

## Rollback
Stop current model and point router to previous passing artifact.
