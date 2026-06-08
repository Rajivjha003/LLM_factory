# 3B QLoRA Failure Audit

## 1. Training Diagnostics
```json
{
  "phase": "Phase 5 - Qwen 3B QLoRA Scaling & Model Selection",
  "run_name": "qwen_3b_qlora_v1_from_sft_v3",
  "base_model": "Qwen/Qwen2.5-3B-Instruct",
  "dataset": "data/sft/merchmix_sft_v3.jsonl",
  "num_train_rows": 500,
  "adapter_dir": "artifacts/adapters/qwen_3b_qlora_v1_from_sft_v3",
  "qlora": {
    "load_in_4bit": true,
    "bnb_4bit_quant_type": "nf4",
    "bnb_4bit_compute_dtype": "bfloat16",
    "bnb_4bit_use_double_quant": true,
    "lora_r": 32,
    "lora_alpha": 64,
    "lora_dropout": 0.05,
    "target_modules": [
      "q_proj",
      "k_proj",
      "v_proj",
      "o_proj",
      "gate_proj",
      "up_proj",
      "down_proj"
    ]
  },
  "training": {
    "max_seq_length": 2048,
    "num_train_epochs": 3,
    "per_device_train_batch_size": 1,
    "gradient_accumulation_steps": 8,
    "learning_rate": 0.0002,
    "warmup_ratio": 0.03,
    "weight_decay": 0.0,
    "lr_scheduler_type": "cosine",
    "logging_steps": 5,
    "save_strategy": "epoch",
    "save_total_limit": 2,
    "bf16": true,
    "fp16": false,
    "gradient_checkpointing": true,
    "optim": "paged_adamw_8bit",
    "max_grad_norm": 0.3,
    "report_to": "none"
  }
}
```
**First Loss:** 3.7711
**Final Loss:** 0.0823
**Conclusion:** Loss converged normally (final loss < 0.5). The training mechanics worked, meaning the failure is likely related to adapter loading, chat templates, or the 3B model's inherent instruction-following characteristics.
**Adapter Size:** 228.44 MB
**Conclusion:** Adapter size is reasonable for 3B.

## 2. Evaluation Diagnostics
- **Total Rows:** 50
- **Pass Rate:** 2.00%
- **Average Score Rate:** 0.00
- **Average Response Length:** 295 chars

**Conclusion:** Response length is normal. The failure might be hallucination, poor instruction following, or an adapter that was not loaded correctly during inference.

### Sample Outputs
**Sample 1 (bq_debug_v3_001):**
```text
Check the unique keys of the joined tables. Ensure the style ID is the primary key in the style master and a distinct field in the sales history. Verify the filter criteria used during joining. ... [truncated]
```

**Sample 2 (bq_debug_v3_002):**
```text
First, ensure the source is filtering by `UPC` or `Inventory ID` as a primary key. If totals match but individual records differ, use `EXCEPT DISTINCT` against the source to find extra rows. Ensure you normalize both sides with `TRIM`, `UPPER`, and sometimes minor regex for edge cases. ... [truncated]
```

**Sample 3 (bq_debug_v3_003):**
```text
A left join retains all records from the left table and matches them against the right table based on a join key. If you add a WHERE clause filtering the right table, only matching rows in the right table are kept. If the join key is not unique or the filter criteria is too broad, the resulting join can appear to remove records. Ensure your join and filter logic align with the data distribution and grain requirements. ... [truncated]
```

**Sample 4 (bq_debug_v3_004):**
```text
Check the following:

1. Null and blank keys.
2. Trailing whitespace.
3. Different casing (upper vs lower).
4. Key length (exact vs substring match).
5. Use of REGEXP_REPLACE for normalization.
6. Incremental watermarks and batch boundaries.
7. Cloud logging for extra read bytes. ... [truncated]
```

**Sample 5 (bq_debug_v3_005):**
```text
Count duplicates by `calendar_week` and `active_csku_count`. If this returns rows where `calendar_week` is mapped to more than one distinct inventory key, the join is multiplying rows. ... [truncated]
```
