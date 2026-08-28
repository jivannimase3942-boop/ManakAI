from fastapi import APIRouter
from ..models import ChatRequest, ChatResponse
from .. import rag

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = rag.answer_query(req.message, req.language)
    return ChatResponse(**result)
