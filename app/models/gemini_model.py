import os

from google import genai

from .base import AIModel


class GeminiModel(AIModel):

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text
