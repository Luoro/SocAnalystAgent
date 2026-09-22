import json
import re

from .base import AIModel


class MockModel(AIModel):

    def generate(self, prompt: str) -> str:

        prompt_lower = prompt.lower()

        # -------------------------
        # FINAL AFTER TOOL
        # -------------------------

        if "tool result:" in prompt_lower:

            tool_result = prompt.split(
                "Tool result:",
                1
            )[1].strip()

            return json.dumps(
                {
                    "action": "final",
                    "answer": (
                        "The SHA256 hash was calculated "
                        f"successfully:\n{tool_result}"
                    )
                }
            )

        # -------------------------
        # HASH TOOL
        # -------------------------

        if "hash" in prompt_lower:

            text_to_hash = self._extract_hash_text(
                prompt
            )

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "calculate_sha256",
                    "arguments": {
                        "text": text_to_hash
                    }
                }
            )

        # -------------------------
        # RAG REQUEST
        # -------------------------

        if (
            "ransomware" in prompt_lower
            and "relevant knowledge" not in prompt_lower
        ):

            return json.dumps(
                {
                    "action": "rag",
                    "query": prompt
                }
            )

        # -------------------------
        # FINAL RESPONSE AFTER RAG
        # -------------------------

        if "relevant knowledge" in prompt_lower:

            return json.dumps(
                {
                    "action": "final",
                    "answer": (
                        "According to the knowledge base, "
                        "the affected endpoint should be "
                        "isolated from the network. "
                        "The security team should preserve "
                        "forensic evidence and investigate "
                        "potential lateral movement."
                    )
                }
            )

        # -------------------------
        # DEFAULT
        # -------------------------

        return json.dumps(
            {
                "action": "final",
                "answer": (
                    "I can answer this question "
                    "without using a tool."
                )
            }
        )

    # -------------------------
    # HASH TEXT EXTRACTION
    # -------------------------

    def _extract_hash_text(
        self,
        prompt: str
    ) -> str:

        patterns = [
            r"hash(?:\s+the)?\s+(?:text\s+)?['\"](.+?)['\"]",
            r"hash(?:\s+the)?\s+(?:text\s+)?(.+?)\s*$",
            r"sha256\s+(?:of|for)\s+['\"](.+?)['\"]",
            r"sha256\s+(?:of|for)\s+(.+?)\s*$",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                prompt,
                re.IGNORECASE
            )

            if match:
                return match.group(1).strip()

        return "hello"