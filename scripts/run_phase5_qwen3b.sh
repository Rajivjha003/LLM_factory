#!/usr/bin/env bash
set -euo pipefail

CONFIG="configs/phase5/qwen3b_qlora_phase5.yaml"

export PYTHONPATH="${PWD}:${PYTHONPATH:-}"

echo "[Phase 5] Downloading Qwen 3B if needed..."
python scripts/download_qwen3b.py --config "$CONFIG"

echo "[Phase 5] Training Qwen 3B QLoRA adapter..."
python scripts/train_qwen3b_qlora.py --config "$CONFIG"

echo "[Phase 5] Evaluating on frozen eval_v3..."
python scripts/eval_qwen3b_eval_v3.py --config "$CONFIG"

echo "[Phase 5] Auditing report math..."
python scripts/audit_phase5_report.py --config "$CONFIG"

echo "[Phase 5] Bootstrapping confidence intervals..."
python scripts/bootstrap_phase5_ci.py --config "$CONFIG"

echo "[Phase 5] Building failure taxonomy..."
python scripts/build_phase5_taxonomy.py --config "$CONFIG"

echo "[Phase 5] Updating model matrix..."
python scripts/update_phase5_model_matrix.py --config "$CONFIG"

echo "[Phase 5] Updating model registry..."
python scripts/update_current_best_model.py --config "$CONFIG"

echo "[Phase 5] Complete. Read reports/model_registry/current_best_model.md"
