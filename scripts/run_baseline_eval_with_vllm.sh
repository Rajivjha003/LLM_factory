#!/bin/bash
MODEL_PATH=$1
EVAL_DIR=$2
OUT_JSONL=$3
OUT_MD=$4

echo "Starting vLLM server for $MODEL_PATH..."
export PATH=/home/rajiv/LLM_Ops_vllm/.venv/lib/python3.11/site-packages/nvidia/cu13/bin:$PATH
export LD_LIBRARY_PATH=/home/rajiv/LLM_Ops_vllm/.venv/lib/python3.11/site-packages/nvidia/cu13/lib:$LD_LIBRARY_PATH
/home/rajiv/LLM_Ops_vllm/.venv/bin/vllm serve "$MODEL_PATH" --host 127.0.0.1 --port 8000 --gpu-memory-utilization 0.60 --max-model-len 2048 > vllm_eval.log 2>&1 &
VLLM_PID=$!

echo "Waiting for vLLM to start..."
while ! curl -s http://127.0.0.1:8000/v1/models > /dev/null; do
  sleep 2
  # Check if vLLM process died
  if ! kill -0 $VLLM_PID 2>/dev/null; then
      echo "vLLM server died. Check vllm_eval.log"
      exit 1
  fi
done
echo "vLLM started!"

echo "Running evaluation..."
python scripts/run_baseline_eval.py --model-path "$MODEL_PATH" --eval-dir "$EVAL_DIR" --output-jsonl "$OUT_JSONL" --output-md "$OUT_MD"

echo "Shutting down vLLM..."
kill $VLLM_PID
wait $VLLM_PID 2>/dev/null
echo "Done."
