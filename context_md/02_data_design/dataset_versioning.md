# Dataset Versioning

## Version Format
`dataset_name_major.minor.patch`

Example:
`sft_sql_retail_v1.0.0`

## Every Dataset Version Must Record
- Source files
- Number of examples
- Domains covered
- Quality score distribution
- PII status
- Train/val/test split
- Creation date
- Author/reviewer

## Rule
No training run may use an unversioned dataset.
