#!/usr/bin/env bash
set -euo pipefail

LLAMA_DIR="${LLAMA_DIR:-/home/rajiv/tools/llama.cpp}"

echo "== Setting up llama.cpp at $LLAMA_DIR =="

mkdir -p "$(dirname "$LLAMA_DIR")"

if [ ! -d "$LLAMA_DIR/.git" ]; then
  git clone https://github.com/ggml-org/llama.cpp "$LLAMA_DIR"
else
  git -C "$LLAMA_DIR" pull
fi

cd "$LLAMA_DIR"

cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j"$(nproc)"

echo "== llama.cpp build complete =="
echo "Binaries:"
ls -lah "$LLAMA_DIR/build/bin" | head

