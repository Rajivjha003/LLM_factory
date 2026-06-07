# Distillation Strategy

## Purpose
Train a smaller student model using outputs from a stronger teacher model.

## Best Use
- Domain-specific assistant
- SQL/reasoning examples
- High-quality SFT generation

## Pipeline
Teacher -> generate examples -> filter/score -> human review -> SFT student -> eval
