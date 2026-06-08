#!/usr/bin/env bash
set -euo pipefail

MERGED_MODEL="${MERGED_MODEL:-artifacts/merged/qwen_1_5b_sft_v2_merged}"
LLAMA_DIR="${LLAMA_DIR:-/home/rajiv/tools/llama.cpp}"
GGUF_DIR="${GGUF_DIR:-models/gguf}"

BASE_GGUF="$GGUF_DIR/qwen_1_5b_sft_v2_merged.F16.gguf"
Q8="$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q8_0.gguf"
Q5="$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q5_K_M.gguf"
Q4="$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q4_K_M.gguf"

mkdir -p "$GGUF_DIR"

if [ ! -d "$LLAMA_DIR" ]; then
  echo "llama.cpp not found at $LLAMA_DIR"
  echo "Run scripts/setup_llama_cpp.sh first."
  exit 1
fi

CONVERT_SCRIPT="$LLAMA_DIR/convert_hf_to_gguf.py"
QUANTIZE_BIN="$LLAMA_DIR/build/bin/llama-quantize"

if [ ! -f "$CONVERT_SCRIPT" ]; then
  echo "Missing converter: $CONVERT_SCRIPT"
  exit 1
fi

if [ ! -x "$QUANTIZE_BIN" ]; then
  echo "Missing quantize binary: $QUANTIZE_BIN"
  echo "Run scripts/setup_llama_cpp.sh first."
  exit 1
fi

echo "== Converting HF merged model to F16 GGUF =="
python "$CONVERT_SCRIPT" "$MERGED_MODEL" --outfile "$BASE_GGUF" --outtype f16

echo "== Quantizing Q8_0 =="
"$QUANTIZE_BIN" "$BASE_GGUF" "$Q8" Q8_0

echo "== Quantizing Q5_K_M =="
"$QUANTIZE_BIN" "$BASE_GGUF" "$Q5" Q5_K_M

echo "== Quantizing Q4_K_M =="
"$QUANTIZE_BIN" "$BASE_GGUF" "$Q4" Q4_K_M

echo "== GGUF artifacts =="
ls -lh "$GGUF_DIR"

