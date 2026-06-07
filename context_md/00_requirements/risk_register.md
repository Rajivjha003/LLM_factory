# Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| GPU OOM | Training fails | Start small, QLoRA, gradient checkpointing, batch size 1 |
| Dependency conflicts | Environment breaks | Use uv, lockfiles, WSL2, separate envs |
| Dataset noise | Bad model behavior | Quality scoring, human curation, eval gate |
| Eval leakage | False confidence | Strict train/eval separation |
| Hallucinated SQL | Wrong outputs | Schema context, SQL verifier, regression tests |
| Unsafe tool use | Production damage | Sandbox, allowlist, human approval |
| Overfitting | Poor generalization | Validation set, early stopping, diverse evals |
| Quantization quality loss | Bad inference | Benchmark Q4/Q5/Q8 and compare |
| MCP prompt injection | Tool misuse | Tool permissions, content isolation, audit logs |
| Context loss across agents | Misguided execution | Use this architecture pack as external memory |
