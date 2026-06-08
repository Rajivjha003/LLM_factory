from pathlib import Path


def test_champion_merged_model_exists():
    path = Path("artifacts/merged/qwen_1_5b_sft_v2_merged")
    assert path.exists()


def test_champion_model_card_exists():
    path = Path("reports/model_registry/qwen_1_5b_sft_v2_champion_model_card.md")
    assert path.exists()


def test_phase7_config_exists():
    path = Path("configs/phase7/phase7_paths.yaml")
    assert path.exists()


def test_gguf_dir_exists_if_quantized():
    # This test is intentionally soft because llama.cpp may not be installed in CI.
    path = Path("models/gguf")
    if path.exists():
        assert path.is_dir()

