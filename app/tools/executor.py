import json

from . import TOOLS


def execute_tool(tool_response: str):

    data = json.loads(tool_response)

    if data.get("type") != "tool_call":
        return data

    tool_name = data["tool"]
    arguments = data.get("arguments", {})

    if tool_name not in TOOLS:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    tool = TOOLS[tool_name]

    function = tool["function"]

    return function(**arguments)
