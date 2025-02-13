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
    response = chat_with_mie(request.prompt, request.session_id, request.api_key)
    if response == "API Key không hợp lệ!":
        raise HTTPException(status_code=403, detail="API Key không hợp lệ!")
    return {"response": response}
