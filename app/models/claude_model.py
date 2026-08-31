import os
import anthropic
from .base import AIModel

class ClaudeModel(AIModel):

    def __init__(self, model_name: str):
        self.model_name = model_name

        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate(self, prompt: str) -> str:

        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text
