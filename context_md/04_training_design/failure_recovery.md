# Failure Recovery

## OOM
Reduce sequence length, batch size, LoRA rank, or model size.

## Loss Explodes
Lower learning rate, check bad data, inspect formatting.

## Model Becomes Verbose
Improve SFT examples and DPO preferences.

## Hallucinated Columns
Add schema-aware evals, negative examples, and verifier penalties.

## Bad Tool Calls
Strengthen tool schemas, permission rules, and tool evals.

## Quantized Model Bad
Try Q5_K_M or Q8_0, compare against unquantized model.
