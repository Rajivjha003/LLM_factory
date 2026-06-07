for i in {1..30}; do
  if curl -s http://127.0.0.1:8000/v1/models > /dev/null; then
    break
  fi
  sleep 5
done

curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "/home/rajiv/models/base/qwen2_5_0_5b_instruct",
    "messages": [
      {"role": "system", "content": "You are a precise data engineering assistant."},
      {"role": "user", "content": "Explain in one paragraph what a BigQuery anti-join is used for."}
    ],
    "temperature": 0.2,
    "max_tokens": 180
  }'
