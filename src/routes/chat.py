from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.chat_handler import chat_with_mie
import time

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    session_id: str
    api_key: str

@router.post("/chat/")
async def chat_with_ai(request: ChatRequest):
    start_time = time.time()
    try:
        response = await chat_with_mie(request.prompt, request.session_id, request.api_key)
        elapsed_time = time.time() - start_time
        return {
            "response": response,
            "response_time": f"{elapsed_time:.2f} s"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
