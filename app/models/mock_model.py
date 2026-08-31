from .base import AIModel


class MockModel(AIModel):

    def generate(self, prompt: str) -> str:
        return (
            "This is a mock response. "
            "The AI model is not connected yet.\n\n"
            f"Received prompt: {prompt}"
        )
