from .agent import Agent


def create_agent(
    model,
    retriever=None,
    tool_executor=None
):

    return Agent(
        model=model,
        retriever=retriever,
        tool_executor=tool_executor
    )