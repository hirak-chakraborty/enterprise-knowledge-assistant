from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


class ChatRequest(BaseModel):
    session_id: str
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    return chat_service.chat(
        session_id=request.session_id,
        question=request.question)