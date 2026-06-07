# Tokenizer Strategy

## For Tiny Scratch Model
Train a tokenizer from scratch using SentencePiece or Hugging Face Tokenizers.

Recommended vocab:
- 16k for tiny models
- 32k for stronger small models

## For Fine-Tuning Existing Models
Do not replace tokenizer unless absolutely necessary. Use the base model tokenizer and chat template.

## SQL/Code Considerations
Prefer tokenizers that handle:
- snake_case
- table.column names
- SQL keywords
- JSON/YAML syntax
- Markdown code fences
