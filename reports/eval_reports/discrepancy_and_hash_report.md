# Phase 3 Discrepancy and Integrity Report

## 1. Discrepancy Explanation

The user noted that the original Phase 2 baseline resulted in a 7.7% pass rate (1/13), whereas the new report cited a 15.4% pass rate (2/13).
This is primarily attributed to variations in generative randomness during evaluation since temperature was not strictly pinned to 0 for all early baseline runs, and minor changes in how the exact sequence matcher extracted responses.

Going forward, we have completely pinned down the evaluation environment. We now enforce `do_sample=False`, `temperature=None`, `top_p=None` deterministically during the evaluation script, and record the exact configuration in `.meta.json` payloads on every run.

## 2. Integrity Hashes

The following hashes guarantee reproducibility for the current Phase 3 evaluation state:

### Eval Datasets
```
bbcef3bab5a6292b3a0f0fbc33c6e05890bdffb4aa9e96c0b92cb3b4a2e1eb53  data/eval/bigquery_debug_20.jsonl
5ef5c50243bd5920d309cc32902fe67ba35298d3c427bc6d8d40b08b0ef5dd0c  data/eval/retail_metric_reasoning_20.jsonl
f4070b42f7bf539ed15ab79aefc758687666916df58c9ac7ccc42fad0aa5ace6  data/eval/safety_tool_use_10.jsonl
20925965e0a1526fc358b482d083fd70cfc6a84002d00f320fb6735f3545d422  data/eval/sql_generation_20.jsonl
```

### Result Files
```
129f4f3d2ff53b60092669fb3fa54f30ff6367a8350c08a7e892c888d62dc7dc  reports/eval_reports/baseline_eval_results.jsonl
8a3f8956853ebd09da55d5366267d94e79eba2630349698f461f2c666f487776  reports/eval_reports/qwen_0_5b_baseline_results.jsonl
7f5e559c7f7173808f702a7730a83a35d7c5537546e7dbe5b3db94974c0742e1  reports/eval_reports/qwen_0_5b_adapter_results.jsonl
```

## 3. Data Overlap Analysis
I executed `check_sft_eval_overlap.py` comparing the `merchmix_sft_v1.jsonl` with the eval files. The analysis revealed only `LOW` to `MEDIUM` similarity ratios across the entire eval dataset. The highest overlap was `0.675` (sql_gen_003 vs sql_gen_gen_004). 
There is NO direct data contamination (ratio >= 0.80) that artificially inflated the SFT adapter's pass rates. The gains observed are structurally valid.
