#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Master model downloader for remaining LLMOps phases
# Downloads sequentially, resumes partial files, retries on failure,
# verifies model folders, and writes a manifest.
# ============================================================

export HF_HOME="${HF_HOME:-/home/rajiv/.cache/huggingface}"
export HF_HUB_ENABLE_HF_TRANSFER=1

MAX_RETRIES="${MAX_RETRIES:-30}"
SLEEP_SECONDS="${SLEEP_SECONDS:-60}"
DOWNLOAD_7B="${DOWNLOAD_7B:-0}"

PROJECT_ROOT="${PROJECT_ROOT:-/home/rajiv/LLM_Ops}"

BASE_MODEL_DIR="/home/rajiv/models/base"
EMBEDDING_MODEL_DIR="/home/rajiv/models/embeddings"
RERANKER_MODEL_DIR="/home/rajiv/models/rerankers"

LOG_DIR="$PROJECT_ROOT/logs/downloads"
MANIFEST_DIR="$PROJECT_ROOT/reports/model_downloads"
MANIFEST_FILE="$MANIFEST_DIR/download_manifest.jsonl"

mkdir -p "$BASE_MODEL_DIR"
mkdir -p "$EMBEDDING_MODEL_DIR"
mkdir -p "$RERANKER_MODEL_DIR"
mkdir -p "$LOG_DIR"
mkdir -p "$MANIFEST_DIR"

cd "$PROJECT_ROOT"

echo "============================================================"
echo "Master Future-Phase Model Downloader"
echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "HF_HOME: $HF_HOME"
echo "MAX_RETRIES: $MAX_RETRIES"
echo "SLEEP_SECONDS: $SLEEP_SECONDS"
echo "DOWNLOAD_7B: $DOWNLOAD_7B"
echo "MANIFEST_FILE: $MANIFEST_FILE"
echo "============================================================"

# Install helper libraries, but don't fail if pip has a temporary issue.
python -m pip install -U "huggingface_hub<1.0" hf_transfer >> "$LOG_DIR/bootstrap.log" 2>&1 || true

download_model() {
  local repo_id="$1"
  local local_dir="$2"
  local purpose="$3"

  local safe_name
  safe_name="$(echo "$repo_id" | tr '/:' '__')"
  local log_file="$LOG_DIR/${safe_name}.log"

  echo ""
  echo "============================================================"
  echo "Downloading: $repo_id"
  echo "Purpose: $purpose"
  echo "Target: $local_dir"
  echo "Log: $log_file"
  echo "============================================================"

  mkdir -p "$local_dir"

  if verify_model_folder "$local_dir" "$repo_id"; then
    echo "Already verified. Skipping: $repo_id"
    write_manifest "$repo_id" "$local_dir" "$purpose" "skipped_already_verified"
    return 0
  fi

  local attempt=1

  while [ "$attempt" -le "$MAX_RETRIES" ]; do
    echo ""
    echo "Attempt $attempt/$MAX_RETRIES for $repo_id at $(date)"
    echo "Attempt $attempt/$MAX_RETRIES for $repo_id at $(date)" >> "$log_file"

    set +e
    python scripts/download_hf_model.py \
      --repo-id "$repo_id" \
      --local-dir "$local_dir" >> "$log_file" 2>&1
    local status=$?
    set -e

    if [ "$status" -eq 0 ]; then
      echo "Download command succeeded for $repo_id."

      if verify_model_folder "$local_dir" "$repo_id"; then
        echo "Verification passed for $repo_id."
        write_manifest "$repo_id" "$local_dir" "$purpose" "downloaded_and_verified"
        return 0
      fi

      echo "Download command succeeded but verification failed. Retrying..."
      echo "Verification failed after successful command." >> "$log_file"
    else
      echo "Download failed with exit code $status for $repo_id."
      echo "Download failed with exit code $status" >> "$log_file"
    fi

    if [ "$attempt" -eq "$MAX_RETRIES" ]; then
      echo "ERROR: Max retries reached for $repo_id."
      echo "Check log: $log_file"
      write_manifest "$repo_id" "$local_dir" "$purpose" "failed"
      return 1
    fi

    echo "Sleeping ${SLEEP_SECONDS}s before retry..."
    sleep "$SLEEP_SECONDS"
    attempt=$((attempt + 1))
  done
}

verify_model_folder() {
  local local_dir="$1"
  local repo_id="$2"

  if [ ! -d "$local_dir" ]; then
    return 1
  fi

  if [ ! -f "$local_dir/config.json" ]; then
    return 1
  fi

  # Tokenizer can vary by model family.
  if [ ! -f "$local_dir/tokenizer.json" ] && \
     [ ! -f "$local_dir/tokenizer.model" ] && \
     [ ! -f "$local_dir/vocab.txt" ]; then
    return 1
  fi

  # Embedding/reranker/LLM models usually have safetensors.
  if ! ls "$local_dir"/*.safetensors >/dev/null 2>&1; then
    return 1
  fi

  # Lightweight config/tokenizer verification.
  set +e
  python - << PY >/tmp/model_verify_stdout.txt 2>/tmp/model_verify_stderr.txt
from transformers import AutoConfig, AutoTokenizer

model_dir = "$local_dir"
repo_id = "$repo_id"

cfg = AutoConfig.from_pretrained(model_dir, trust_remote_code=True)
tok = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

print("repo_id=", repo_id)
print("model_type=", getattr(cfg, "model_type", None))
print("hidden_size=", getattr(cfg, "hidden_size", None))
print("num_hidden_layers=", getattr(cfg, "num_hidden_layers", None))
print("tokenizer_size=", len(tok))
PY
  local verify_status=$?
  set -e

  if [ "$verify_status" -ne 0 ]; then
    echo "Transformers config/tokenizer verification failed for $repo_id"
    cat /tmp/model_verify_stderr.txt || true
    return 1
  fi

  return 0
}

write_manifest() {
  local repo_id="$1"
  local local_dir="$2"
  local purpose="$3"
  local status="$4"

  local size
  size="$(du -sh "$local_dir" 2>/dev/null | awk '{print $1}' || echo unknown)"

  python - << PY
import json
from datetime import datetime, timezone
from pathlib import Path

manifest = Path("$MANIFEST_FILE")
record = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "repo_id": "$repo_id",
    "local_dir": "$local_dir",
    "purpose": "$purpose",
    "status": "$status",
    "size": "$size",
}
with manifest.open("a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
print(json.dumps(record, indent=2))
PY
}

echo ""
echo "Download queue:"
echo "1. Qwen/Qwen2.5-3B-Instruct"
echo "2. BAAI/bge-small-en-v1.5"
echo "3. BAAI/bge-base-en-v1.5"
echo "4. BAAI/bge-reranker-base"
if [ "$DOWNLOAD_7B" = "1" ]; then
  echo "5. Qwen/Qwen2.5-7B-Instruct"
else
  echo "5. Qwen/Qwen2.5-7B-Instruct SKIPPED unless DOWNLOAD_7B=1"
fi

download_model \
  "Qwen/Qwen2.5-3B-Instruct" \
  "$BASE_MODEL_DIR/qwen2_5_3b_instruct" \
  "Phase 5 Qwen 3B QLoRA scaling experiment"

download_model \
  "BAAI/bge-small-en-v1.5" \
  "$EMBEDDING_MODEL_DIR/bge-small-en-v1.5" \
  "Phase 8 RAG lightweight embeddings"

download_model \
  "BAAI/bge-base-en-v1.5" \
  "$EMBEDDING_MODEL_DIR/bge-base-en-v1.5" \
  "Phase 8 RAG stronger embeddings"

download_model \
  "BAAI/bge-reranker-base" \
  "$RERANKER_MODEL_DIR/bge-reranker-base" \
  "Phase 8 RAG reranker"

if [ "$DOWNLOAD_7B" = "1" ]; then
  download_model \
    "Qwen/Qwen2.5-7B-Instruct" \
    "$BASE_MODEL_DIR/qwen2_5_7b_instruct" \
    "Future optional 7B QLoRA scaling experiment"
else
  echo ""
  echo "Skipping Qwen 7B because DOWNLOAD_7B is not 1."
fi

echo ""
echo "============================================================"
echo "All requested downloads completed."
echo "Manifest: $MANIFEST_FILE"
echo "============================================================"

echo ""
echo "Downloaded model sizes:"
du -sh "$BASE_MODEL_DIR"/* 2>/dev/null || true
du -sh "$EMBEDDING_MODEL_DIR"/* 2>/dev/null || true
du -sh "$RERANKER_MODEL_DIR"/* 2>/dev/null || true

echo ""
echo "Next Phase 5 command:"
echo "python scripts/run_sft_qlora.py --config configs/training/sft_qwen_3b_qlora_v1.yaml"
