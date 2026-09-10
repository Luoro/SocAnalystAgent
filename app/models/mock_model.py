import json

from .base import AIModel


class MockModel(AIModel):

    def generate(self, prompt: str) -> str:

        prompt_lower = prompt.lower()

        if "ransomware" in prompt_lower:

            return json.dumps(
                {
                    "action": "rag",
                    "query": prompt
                }
            )

        if "hash" in prompt_lower:

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "calculate_sha256",
                    "arguments": {
                        "text": "hello"
                    }
                }
            )

        return json.dumps(
            {
                "action": "final",
                "answer": (
                    "I can answer this question "
                    "without using a tool."
                )
            }
        )
