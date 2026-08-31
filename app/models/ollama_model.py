import os

from openai import OpenAI

from .base import AIModel


class OllamaModel(AIModel):

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = OpenAI(
            base_url=os.getenv(
                "OLLAMA_HOST",
                "http://localhost:11434"
            ) + "/v1",
            api_key="ollama"
        )

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content
