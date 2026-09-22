import json


def parse_action(response: str) -> dict:

    try:

        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "action": "final",
            "answer": response
        }