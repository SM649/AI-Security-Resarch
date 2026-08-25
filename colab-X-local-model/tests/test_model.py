from unittest.mock import MagicMock, patch

from model import load_model


def test_generate_calls_pipeline_with_prompt_and_returns_text():
    fake_pipeline = MagicMock(
        return_value=[{"generated_text": "hello there"}]
    )
    with patch("model.pipeline", return_value=fake_pipeline) as mock_pipeline_factory:
        hf_model = load_model("gpt2")
        result = hf_model.generate("hello", max_new_tokens=10)

    mock_pipeline_factory.assert_called_once_with("text-generation", model="gpt2")
    fake_pipeline.assert_called_once_with(
        "hello", max_new_tokens=10, num_return_sequences=1
    )
    assert result == "hello there"


def test_generate_strips_prompt_prefix_when_model_echoes_it():
    fake_pipeline = MagicMock(
        return_value=[{"generated_text": "hello there, how are you?"}]
    )
    with patch("model.pipeline", return_value=fake_pipeline):
        hf_model = load_model("gpt2")
        result = hf_model.generate("hello", max_new_tokens=10)

    assert result == "there, how are you?"
