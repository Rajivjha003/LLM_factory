# LLMOps REST API Documentation

This document outlines the REST API endpoints available in the LLMOps platform. The API provides endpoints to manage data validation, trigger training runs, and run evaluations asynchronously.

Base URL locally: `http://localhost:8000`

---

## 1. Data Endpoints

### 1.1 Validate Dataset
`POST /api/v1/data/validate`
Validates a JSONL dataset file against the `SFTSample` Pydantic schema and security rules (blocking DROP/DELETE SQL).

**Request Body**
```json
{
  "file_path": "data/sft/merchmix_sft_v1.jsonl"
}
```

**Response**
```json
{
  "status": "success",
  "valid_count": 105,
  "message": "All samples are valid and safe."
}
```

### 1.2 Inspect Dataset
`GET /api/v1/data/inspect?file_path=data/sft/merchmix_sft_v1.jsonl`
Returns domain distribution, difficulty counts, and assistant response length statistics.

---

## 2. Training Endpoints

### 2.1 Start LoRA Fine-Tuning
`POST /api/v1/train/lora`
Starts an asynchronous training run using QLoRA/LoRA on the specified configuration. Returns a background `job_id`.

**Request Body**
```json
{
  "config_path": "configs/training/sft_qwen_0_5b_lora.yaml"
}
```

**Response**
```json
{
  "status": "accepted",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "LoRA training started in background."
}
```

### 2.2 Check Training Status
`GET /api/v1/train/status/{job_id}`
Returns the current status of the requested background training job (`pending`, `running`, `completed`, `failed`).

---

## 3. Evaluation Endpoints

### 3.1 Start Adapter Evaluation
`POST /api/v1/eval/run`
Starts an asynchronous evaluation benchmark for a trained adapter against the baseline.

**Request Body**
```json
{
  "base_model": "/home/rajiv/models/base/qwen2_5_0_5b_instruct",
  "adapter": "models/adapters/qwen_0_5b_merchmix_v1",
  "eval_dir": "data/eval",
  "output_jsonl": "reports/eval_reports/qwen_0_5b_adapter_results.jsonl"
}
```

**Response**
```json
{
  "status": "accepted",
  "job_id": "112e8400-e29b-41d4-a716-446655441111",
  "message": "Evaluation started in background."
}
```

### 3.2 Compare Evaluation Runs
`POST /api/v1/eval/compare`
Compares a baseline JSONL evaluation report against a candidate adapter JSONL report and returns the pass/fail diffs.

**Request Body**
```json
{
  "baseline": "reports/eval_reports/qwen_0_5b_baseline_results.jsonl",
  "candidate": "reports/eval_reports/qwen_0_5b_adapter_results.jsonl",
  "output_md": "reports/eval_reports/comparison_report.md"
}
```
