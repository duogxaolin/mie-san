import os
import ollama
from src.faiss_index import search_faiss
from src.database import get_db_connection
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def verify_api_key(api_key):
    """ Kiểm tra API Key hợp lệ trong MySQL """
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT 1 FROM users WHERE api_key = %s LIMIT 1", (api_key,))
        result = await cursor.fetchone()
    await conn.ensure_closed()
    return result is not None

async def get_chat_history(session_id):
    """ Lấy lịch sử chat từ MySQL theo session_id (tối ưu hơn) """
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT role, message FROM chats WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
        return [{"role": role, "content": message} for role, message in await cursor.fetchall()]
    await conn.ensure_closed()

async def chat_with_mie(prompt: str, session_id: str, api_key: str) -> str:
    """ Xử lý hội thoại với chatbot Mie-san qua Ollama """
    if not await verify_api_key(api_key):
        return "API Key không hợp lệ!"

    # Load lịch sử chat & tìm kiếm thông tin liên quan
    chat_history_task = get_chat_history(session_id)
    related_info_task = search_faiss(prompt)  # Nếu FAISS hoạt động

    chat_history, related_info = await asyncio.gather(chat_history_task, related_info_task)

    # Chuẩn bị tin nhắn cho mô hình
    messages = [{"role": "system", "content": "Bạn là một trợ lý AI thông minh."}]
    messages.extend(chat_history)

    user_message = {"role": "user", "content": prompt}
    if related_info:
        user_message["content"] += f"\nThông tin liên quan: {related_info}"
    messages.append(user_message)

    # Gọi Ollama (không cần API Key)
    try:
        response = ollama.chat(model="gemma2:2b", messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"Lỗi khi gọi Ollama: {str(e)}"
