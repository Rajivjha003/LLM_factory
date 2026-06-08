#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Phase 5 model downloader with auto-retry and resume support
# ============================================================

export HF_HOME="${HF_HOME:-/home/rajiv/.cache/huggingface}"
export HF_HUB_ENABLE_HF_TRANSFER=1

MAX_RETRIES="${MAX_RETRIES:-20}"
SLEEP_SECONDS="${SLEEP_SECONDS:-60}"

MODEL_REPO="Qwen/Qwen2.5-3B-Instruct"
MODEL_DIR="/home/rajiv/models/base/qwen2_5_3b_instruct"

LOG_DIR="logs/downloads"
LOG_FILE="${LOG_DIR}/qwen_3b_download.log"

mkdir -p "$MODEL_DIR"
mkdir -p "$LOG_DIR"

echo "============================================================"
echo "Phase 5 Download: $MODEL_REPO"
echo "Target dir: $MODEL_DIR"
echo "HF_HOME: $HF_HOME"
echo "Max retries: $MAX_RETRIES"
echo "Sleep between retries: ${SLEEP_SECONDS}s"
echo "Log file: $LOG_FILE"
echo "============================================================"

# Install/upgrade helpers if available. Do not fail the script if this step has issues.
python -m pip install -U huggingface_hub hf_transfer >> "$LOG_FILE" 2>&1 || true

attempt=1

while [ "$attempt" -le "$MAX_RETRIES" ]; do
  echo ""
  echo "Attempt $attempt/$MAX_RETRIES at $(date)"
  echo "Attempt $attempt/$MAX_RETRIES at $(date)" >> "$LOG_FILE"

  set +e
  python scripts/download_hf_model.py \
    --repo-id "$MODEL_REPO" \
    --local-dir "$MODEL_DIR" >> "$LOG_FILE" 2>&1
  status=$?
  set -e

  if [ "$status" -eq 0 ]; then
    echo "Download command succeeded."
    break
  fi

  echo "Download failed with exit code $status."
  echo "Download failed with exit code $status." >> "$LOG_FILE"

  if [ "$attempt" -eq "$MAX_RETRIES" ]; then
    echo "ERROR: Max retries reached. Check log: $LOG_FILE"
    exit 1
  fi

  echo "Sleeping ${SLEEP_SECONDS}s before retry..."
  sleep "$SLEEP_SECONDS"

  attempt=$((attempt + 1))
done

echo ""
echo "Downloaded folder size:"
du -sh "$MODEL_DIR" || true

echo ""
echo "Files:"
ls -lah "$MODEL_DIR" || true

echo ""
echo "Verifying required model files..."

missing=0

if [ ! -f "$MODEL_DIR/config.json" ]; then
  echo "MISSING: config.json"
  missing=1
fi

if [ ! -f "$MODEL_DIR/tokenizer.json" ] && [ ! -f "$MODEL_DIR/tokenizer.model" ]; then
  echo "MISSING: tokenizer.json or tokenizer.model"
  missing=1
fi

if ! ls "$MODEL_DIR"/*.safetensors >/dev/null 2>&1; then
  echo "MISSING: safetensors model files"
  missing=1
fi

if [ "$missing" -eq 1 ]; then
  echo "ERROR: Download folder is incomplete."
  echo "Rerun this script. Hugging Face should resume the partial download."
  exit 1
fi

echo ""
echo "Running lightweight Transformers load verification..."

python - << PY
from transformers import AutoTokenizer, AutoConfig

model_dir = "$MODEL_DIR"

tok = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
cfg = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)

print("Verification passed.")
print("Model type:", getattr(cfg, "model_type", None))
print("Hidden size:", getattr(cfg, "hidden_size", None))
print("Num layers:", getattr(cfg, "num_hidden_layers", None))
print("Vocab size:", getattr(cfg, "vocab_size", None))
print("Tokenizer vocab size:", len(tok))
PY

echo ""
echo "SUCCESS: $MODEL_REPO is downloaded and verified at:"
echo "$MODEL_DIR"
echo ""
echo "Next step:"
echo "python scripts/run_sft_qlora.py --config configs/training/sft_qwen_3b_qlora_v1.yaml"
