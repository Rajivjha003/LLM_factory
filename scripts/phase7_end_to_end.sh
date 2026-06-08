#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=src

echo "== Phase 7: Champion Packaging + Quantization =="

CONFIG="configs/phase7/phase7_paths.yaml"
MERGED_MODEL="artifacts/merged/qwen_1_5b_sft_v2_merged"
BASE_MODEL="/home/rajiv/models/base/qwen2_5_1_5b_instruct"
SFT_ADAPTER="artifacts/adapters/qwen_1_5b_sft_v2_failure_driven"

echo "1. Build model card"
python scripts/build_champion_model_card.py --config "$CONFIG"

echo "2. Ensure merged champion exists"
if [ ! -d "$MERGED_MODEL" ]; then
  python scripts/merge_lora_adapter.py \
    --base-model "$BASE_MODEL" \
    --adapter "$SFT_ADAPTER" \
    --output-model "$MERGED_MODEL"
else
  echo "Merged model already exists: $MERGED_MODEL"
fi

echo "3. Verify merged model"
python scripts/verify_merged_model.py --model "$MERGED_MODEL"

echo "4. Benchmark HF inference"
python scripts/benchmark_hf_inference.py \
  --model "$MERGED_MODEL" \
  --output-json reports/benchmarks/qwen_1_5b_sft_v2_hf_benchmark.json

echo "5. Evaluate merged model with Judge v3"
python scripts/run_merged_eval_v3.py \
  --model "$MERGED_MODEL" \
  --eval-dir data/eval_v3 \
  --output-jsonl reports/eval_reports/qwen_1_5b_sft_v2_merged_eval_v3_judge_v3.jsonl \
  --output-md reports/eval_reports/qwen_1_5b_sft_v2_merged_eval_v3_judge_v3.md \
  --metadata-json reports/eval_reports/qwen_1_5b_sft_v2_merged_eval_v3_judge_v3.metadata.json

echo "6. Build llama.cpp"
./scripts/setup_llama_cpp.sh

echo "7. Convert and quantize GGUF"
./scripts/convert_and_quantize_champion_gguf.sh

echo "8. Benchmark quantized models"
./scripts/benchmark_llama_cpp_quantized.sh

echo "9. Build package manifest"
python scripts/build_model_package_manifest.py --config "$CONFIG"

echo "10. Tests"
pytest tests/test_phase7_packaging.py

echo "== Phase 7 complete =="

