#!/usr/bin/env bash
set -euo pipefail

LLAMA_DIR="${LLAMA_DIR:-/home/rajiv/tools/llama.cpp}"
GGUF_DIR="${GGUF_DIR:-models/gguf}"
OUT_MD="${OUT_MD:-reports/benchmarks/qwen_1_5b_sft_v2_quantized_benchmark.md}"

LLAMA_CLI="$LLAMA_DIR/build/bin/llama-cli"

if [ ! -x "$LLAMA_CLI" ]; then
  echo "Missing llama-cli: $LLAMA_CLI"
  echo "Run scripts/setup_llama_cpp.sh first."
  exit 1
fi

mkdir -p "$(dirname "$OUT_MD")"

PROMPT="You are a precise retail data engineering assistant for Merchmix. Give safe BigQuery SQL to find duplicate normalized inventory IDs and include interpretation."

{
  echo "# Quantized llama.cpp Benchmark"
  echo ""
  echo "Prompt:"
  echo ""
  echo '```text'
  echo "$PROMPT"
  echo '```'
  echo ""
  echo "| Model | Result |"
  echo "|---|---|"
} > "$OUT_MD"

for model in \
  "$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q8_0.gguf" \
  "$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q5_K_M.gguf" \
  "$GGUF_DIR/qwen_1_5b_sft_v2_merged.Q4_K_M.gguf"
do
  if [ ! -f "$model" ]; then
    echo "Skipping missing model: $model"
    continue
  fi

  echo "== Benchmarking $model =="

  set +e
  output="$("$LLAMA_CLI" -m "$model" -p "$PROMPT" -n 256 --temp 0 2>&1)"
  status=$?
  set -e

  escaped="$(echo "$output" | head -c 3000 | tr '\n' ' ' | sed 's/|/\\|/g')"

  if [ "$status" -eq 0 ]; then
    echo "| \`$model\` | $escaped |" >> "$OUT_MD"
  else
    echo "| \`$model\` | FAILED: $escaped |" >> "$OUT_MD"
  fi
done

echo "Wrote $OUT_MD"

