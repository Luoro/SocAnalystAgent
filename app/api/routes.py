from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# Esta variable será configurada desde main.py
agent = None


@router.get("/health")
def health():
    return {
        "status": "ok"
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if agent is None:
        return ChatResponse(
            response="Agent is not initialized."
        )

    response = agent.run(
        request.message
    )

    return ChatResponse(
        response=response
    )
