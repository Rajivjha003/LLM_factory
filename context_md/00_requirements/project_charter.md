# Project Charter

## Project Name
Local-First 2026 SLLM Factory

## Mission
Build an end-to-end local-first LLM engineering system that can train tiny models from scratch, fine-tune open SLLMs, align them using preference and verifier-based methods, compress them for local/API inference, serve them through production-grade endpoints, connect them to tools safely, and continuously evaluate and improve them.

## Primary User
A high-capacity AI/data engineer working on retail data engineering, BigQuery/Postgres pipelines, SQL debugging, WSSI, ETL architecture, RAG, and agentic AI systems.

## Primary Outcome
A reproducible, hardware-aware LLMOps architecture that turns a single RTX 4090 Laptop machine into a serious SLLM research and deployment lab.

## Non-Goals
- Training a frontier-scale generic LLM from scratch locally.
- Full fine-tuning large 7B+ models without adapters.
- Blind RLHF/PPO before simpler alignment methods.
- Unsafe direct tool execution.
- Premature pruning before quantization/evaluation.

## First Serious Model Target
`Merchmix-SQL-Retail-Reasoner-7B`

## Model Purpose
Specialized assistant for:
- BigQuery SQL
- Postgres SQL
- Bronze/Silver/Gold pipelines
- Retail sales, stock, purchase order, and WSSI logic
- Data reconciliation
- Cloud Run / scheduler debugging
- ETL architecture
- Schema understanding
- Agentic tool use

## Success Definition
The system is successful when it can repeatedly produce, evaluate, serve, and improve specialized SLLMs without losing project context, hardware limits, safety rules, or evaluation discipline.
