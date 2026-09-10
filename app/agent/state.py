from dataclasses import dataclass, field


@dataclass
class AgentState:

    user_input: str

    messages: list = field(
        default_factory=list
    )

    tool_calls: list = field(
        default_factory=list
    )

    retrieved_documents: list = field(
        default_factory=list
    )

    final_answer: str | None = None
