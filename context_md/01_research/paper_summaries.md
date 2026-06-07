# Paper and Method Summaries

## LoRA
Low-Rank Adaptation trains small adapter matrices instead of full model weights. Use for efficient fine-tuning.

## QLoRA
Quantized LoRA freezes the base model in low precision and trains adapters. Use for 7B/8B local fine-tuning on 16 GB VRAM.

## DPO
Direct Preference Optimization trains from chosen/rejected pairs without full RLHF complexity. Use after SFT.

## PPO/RLHF
Powerful but memory-heavy and operationally complex. Not first choice for local 16 GB VRAM workflows.

## GRPO/RLVR
Verifier/reward-based training for tasks where correctness can be measured. Useful for SQL/code/reasoning.

## RAG
Retrieval-Augmented Generation supplies external factual knowledge. Use for facts and project context instead of fine-tuning every fact.

## Quantization
Reduces model memory and improves deployment feasibility. Must always be evaluated for quality loss.
