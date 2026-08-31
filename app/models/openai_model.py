import os
from openai import OpenAI
from .base import AIModel


class OpenAIModel(AIModel):

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate(self, prompt: str) -> str:

        response = self.client.responses.create(
            model=self.model_name,
            input=prompt
        )

        return response.output_text
