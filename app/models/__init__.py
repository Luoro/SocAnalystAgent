import os

from .base import AIModel
from .openai_model import OpenAIModel
from .claude_model import ClaudeModel
from .gemini_model import GeminiModel
from .ollama_model import OllamaModel
from .mock_model import MockModel

def get_model(provider: str) -> AIModel:
    if provider == "mock":
        return MockModel()

    if provider == "openai":
        return OpenAIModel(
            model_name=os.getenv("OPENAI_MODEL")
        )

    if provider == "claude":
        return ClaudeModel(
            model_name=os.getenv("CLAUDE_MODEL")
        )

    if provider == "gemini":
        return GeminiModel(
            model_name=os.getenv("GEMINI_MODEL")
        )

    if provider == "ollama":
        return OllamaModel(
            model_name=os.getenv("OLLAMA_MODEL")
        )

    raise ValueError(
        f"Unsupported model provider: {provider}"
    )
