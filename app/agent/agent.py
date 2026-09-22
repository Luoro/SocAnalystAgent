from .state import AgentState
from .action_parser import parse_action


class Agent:

    def __init__(
        self,
        model,
        retriever=None,
        tool_executor=None
    ):

        self.model = model
        self.retriever = retriever
        self.tool_executor = tool_executor

    def run(
        self,
        user_input: str,
        max_iterations: int = 5
    ) -> str:

        state = AgentState(
            user_input=user_input
        )

        current_input = user_input

        for _ in range(max_iterations):

            response = self.model.generate(
                current_input
            )

            action = parse_action(
                response
            )

            action_type = action.get(
                "action"
            )

            # -------------------------
            # FINAL
            # -------------------------

            if action_type == "final":

                state.final_answer = (
                    action.get("answer", "")
                )

                return state.final_answer

            # -------------------------
            # RAG
            # -------------------------

            if action_type == "rag":

                if self.retriever is None:
                    return (
                        "RAG is not available."
                    )

                query = action.get(
                    "query",
                    user_input
                )

                results = self.retriever.search(
                    query
                )

                state.retrieved_documents = (
                    results
                )

                context = "\n\n".join(
                    result["text"]
                    for result in results
                )

                current_input = f"""
User question:

{user_input}

Relevant knowledge:

{context}

Based on this information,
provide the final answer.
"""

                continue

            # -------------------------
            # TOOL
            # -------------------------

            if action_type == "tool":

                if self.tool_executor is None:
                    return (
                        "Tools are not available."
                    )

                tool_name = action.get(
                    "tool"
                )

                arguments = action.get(
                    "arguments",
                    {}
                )

                result = (
                    self.tool_executor(
                        tool_name,
                        arguments
                    )
                )

                state.tool_calls.append(
                    {
                        "tool": tool_name,
                        "result": result
                    }
                )

                current_input = f"""
User question:

{user_input}

Tool used:

{tool_name}

Tool result:

{result}

Provide the final answer.
"""

                continue

            return (
                "The agent returned an "
                "unsupported action."
            )

        return (
            "The agent reached the maximum "
            "number of iterations."
        )