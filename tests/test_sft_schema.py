import pytest
from pydantic import ValidationError

from llm_ops.data.sft_schemas import SFTSample


def test_valid_sft_sample():
    row = {
        "id": "test_001",
        "domain": "bigquery_debugging",
        "difficulty": "easy",
        "source": "manual",
        "messages": [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "User prompt"},
            {"role": "assistant", "content": "Assistant answer"},
        ],
    }

    sample = SFTSample.model_validate(row)

    assert sample.id == "test_001"
    assert sample.messages[0].role == "system"
    assert sample.messages[-1].role == "assistant"


def test_first_message_must_be_system():
    row = {
        "id": "test_002",
        "domain": "bigquery_debugging",
        "difficulty": "easy",
        "source": "manual",
        "messages": [
            {"role": "user", "content": "User prompt"},
            {"role": "assistant", "content": "Assistant answer"},
        ],
    }

    with pytest.raises(ValidationError):
        SFTSample.model_validate(row)


def test_last_message_must_be_assistant():
    row = {
        "id": "test_003",
        "domain": "bigquery_debugging",
        "difficulty": "easy",
        "source": "manual",
        "messages": [
            {"role": "system", "content": "System prompt"},
            {"role": "user", "content": "User prompt"},
        ],
    }

    with pytest.raises(ValidationError):
        SFTSample.model_validate(row)
