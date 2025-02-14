import os
import ollama
from src.faiss_index import search_faiss
from dotenv import load_dotenv
import asyncio
os.environ["OLLAMA_ACCELERATE"] = "1"
# Import các repository đã được xây dựng trong repositories.py (xem file bên dưới)
from src.repositories import UserRepository, ChatRepository
from src.database import db_manager

load_dotenv()

# Khởi tạo các repository với db_manager đã tạo pool
user_repo = UserRepository(db_manager)
chat_repo = ChatRepository(db_manager)

async def verify_api_key(api_key: str) -> bool:
    user = await user_repo.get_user_by_api_key(api_key)
    return bool(user)

async def get_chat_history(session_id: str):
    return await chat_repo.get_chat_history(session_id)

async def chat_with_mie(prompt: str, session_id: str, api_key: str) -> str:
    if not await verify_api_key(api_key):
        return "API Key không hợp lệ!"

    # Song song: lấy lịch sử chat và tìm dữ liệu liên quan qua FAISS
    chat_history_task = get_chat_history(session_id)
    related_info_task = search_faiss(prompt)

    chat_history, related_info = await asyncio.gather(chat_history_task, related_info_task)

    # Chuẩn bị danh sách message cho mô hình Ollama
    messages = []
    messages.extend(chat_history)
    user_message = {"role": "user", "content": prompt}
    if related_info:
        user_message["content"] += f"\nThông tin liên quan: {related_info}"
    messages.append(user_message)

    try:
        response = ollama.chat(model="gemma2", messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"Lỗi khi gọi Ollama: {str(e)}"
