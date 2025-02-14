from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.chat_handler import chat_with_mie

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    session_id: str
    api_key: str

@router.post("/chat/")
async def chat_with_ai(request: ChatRequest):
    try:
        response = chat_with_mie(request.prompt, request.session_id, request.api_key)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
