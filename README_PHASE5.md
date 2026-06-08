# Phase 5 - Qwen 3B QLoRA Scaling & Model Selection

This pack adds the Phase 5 controlled scaling experiment:

- Base: `Qwen/Qwen2.5-3B-Instruct`
- Method: 4-bit QLoRA
- Dataset: `data/sft/merchmix_sft_v3.jsonl`
- Benchmark: frozen `data/eval/eval_v3.jsonl`
- Judge: deterministic Judge v2-style rubric scorer
- Champion to beat: Qwen 1.5B SFT v2 at 34% pass / 92.7% score

## Install

```bash
cd ~/llm-lab
source .venv/bin/activate
pip install -r requirements_phase5.txt
```

## Run full Phase 5

```bash
bash scripts/run_phase5_qwen3b.sh
```

## Run manually

```bash
python scripts/download_qwen3b.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/train_qwen3b_qlora.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/eval_qwen3b_eval_v3.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/audit_phase5_report.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/bootstrap_phase5_ci.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/build_phase5_taxonomy.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/update_phase5_model_matrix.py --config configs/phase5/qwen3b_qlora_phase5.yaml
python scripts/update_current_best_model.py --config configs/phase5/qwen3b_qlora_phase5.yaml
```
