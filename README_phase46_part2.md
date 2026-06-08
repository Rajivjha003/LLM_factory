# Phase 4.6 Part 2 Package

This package contains the corrected, complete files for the Phase 4.6 SFT v4 pipeline.

## Files

- `scripts/generate_rubric_sft_v4_additions.py`
- `data/sft/real_world_clean/real_world_sft_v4_additions.jsonl`
- `scripts/build_sft_v4.py`
- `scripts/validate_sft_v4_quality.py`
- `configs/training/sft_qwen_1_5b_lora_v4.yaml`
- `scripts/phase46_sft_v4_end_to_end.sh`
- `tests/test_sft_v4_quality.py`

## Install into repo

Copy or unzip the contents into `~/LLM_Ops`, preserving folders.

```bash
cd ~/LLM_Ops
unzip /path/to/phase46_part2_package.zip -d .
chmod +x scripts/phase46_sft_v4_end_to_end.sh
```

Then run:

```bash
source .venv/bin/activate
python scripts/generate_rubric_sft_v4_additions.py \
  --output data/sft/generated/rubric_sft_v4_additions.jsonl \
  --count 300 \
  --seed 42

python scripts/build_sft_v4.py \
  --base-sft data/sft/merchmix_sft_v3.jsonl \
  --rubric-additions data/sft/generated/rubric_sft_v4_additions.jsonl \
  --real-additions data/sft/real_world_clean/real_world_sft_v4_additions.jsonl \
  --output data/sft/merchmix_sft_v4.jsonl \
  --target-count 900

python scripts/validate_sft_data.py --path data/sft/merchmix_sft_v4.jsonl
python scripts/validate_sft_v4_quality.py \
  --sft data/sft/merchmix_sft_v4.jsonl \
  --output-md reports/sft_quality/sft_v4_quality_report.md \
  --min-count 800

pytest tests/test_sft_v4_quality.py
```

For full execution:

```bash
./scripts/phase46_sft_v4_end_to_end.sh
```
