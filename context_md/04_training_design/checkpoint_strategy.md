# Checkpoint Strategy

## Save Types
- Adapter checkpoints
- Full merged model only after successful eval
- Training state for resume
- Best model by validation score
- Final model after release gate

## Save Frequency
- Small experiments: every epoch
- Larger runs: periodic step checkpoints
- Always save best validation checkpoint

## Artifact Naming
`modelname_method_datasetversion_date_runid`

## Rule
Never overwrite the previous best model.
