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
                        "The tool executed successfully.\n\n"
                        f"Result:\n{tool_result}"
                    )
                }
            )

        # -------------------------
        # IP REPUTATION
        # -------------------------

        if (
            "ip reputation" in prompt_lower
            or "reputation of" in prompt_lower
            or "reputation for" in prompt_lower
        ):

            match = re.search(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                prompt
            )

            if match:

                return json.dumps(
                    {
                        "action": "tool",
                        "tool": "check_ip_reputation",
                        "arguments": {
                            "ip": match.group(0)
                        }
                    }
                )

        # -------------------------
        # DOMAIN RESOLUTION
        # -------------------------

        if (
            "resolve domain" in prompt_lower
            or "resolve" in prompt_lower
            or "dns" in prompt_lower
        ):

            match = re.search(
                r"\b(?:[a-zA-Z0-9-]+\.)+"
                r"[a-zA-Z]{2,}\b",
                prompt
            )

            if match:

                return json.dumps(
                    {
                        "action": "tool",
                        "tool": "resolve_domain",
                        "arguments": {
                            "domain": match.group(0)
                        }
                    }
                )

        # -------------------------
        # MITRE
        # -------------------------

        if (
            "mitre" in prompt_lower
            or "attack technique" in prompt_lower
        ):

            technique = prompt.strip()

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "search_mitre_technique",
                    "arguments": {
                        "technique": technique
                    }
                }
            )

        # -------------------------
        # FILE HASH
        # -------------------------

        if (
            "file hash" in prompt_lower
            or "calculate file hash" in prompt_lower
        ):

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "calculate_file_hash",
                    "arguments": {
                        "file_path": "sample.txt",
                        "algorithm": "sha256"
                    }
                }
            )

        # -------------------------
        # PCAP
        # -------------------------

        if (
            "pcap" in prompt_lower
            or "packet capture" in prompt_lower
        ):

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "analyze_pcap",
                    "arguments": {
                        "file_path": "capture.pcap"
                    }
                }
            )

        # -------------------------
        # LOG SEARCH
        # -------------------------

        if (
            "search logs" in prompt_lower
            or "search the logs" in prompt_lower
        ):

            return json.dumps(
                {
                    "action": "tool",
                    "tool": "search_logs",
                    "arguments": {
                        "query": prompt
                    }
                }
            )

        # -------------------------
        # HASH TEXT
        # -------------------------

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

        # -------------------------
        # RAG
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
        # FINAL AFTER RAG
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