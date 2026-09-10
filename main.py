import os

from dotenv import load_dotenv

from app.models import get_model

from app.rag import build_knowledge_base
from app.rag.retriever import Retriever

from app.agent import create_agent

from app.tools.executor import execute_tool


load_dotenv()


# -------------------------
# MODEL
# -------------------------

provider = os.getenv(
    "MODEL_PROVIDER",
    "mock"
)

model = get_model(provider)


# -------------------------
# RAG
# -------------------------

vector_store, embedding_model = (
    build_knowledge_base(
        "knowledge"
    )
)

retriever = Retriever(
    vector_store,
    embedding_model
)


# -------------------------
# AGENT
# -------------------------

agent = create_agent(
    model=model,
    retriever=retriever,
    tool_executor=execute_tool
)


# -------------------------
# USER
# -------------------------

question = input(
    "Ask the SOC Agent: "
)


answer = agent.run(
    question
)


print("\nAgent:")
print(answer)
