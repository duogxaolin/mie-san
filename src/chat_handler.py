import os
from openai import OpenAI
from src.faiss_index import search_faiss
from src.database import get_db_connection
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("OLLAMA_API_KEY", "duogxaolin")

client_ollama = OpenAI(
    base_url=API_URL,
    api_key=API_KEY
)

async def verify_api_key(api_key):
    """ Kiểm tra API Key trong MySQL """
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT COUNT(*) FROM users WHERE api_key = %s", (api_key,))
        result = await cursor.fetchone()
    await conn.ensure_closed()
    return result[0] > 0

async def get_chat_history(session_id):
    """ Lấy lịch sử chat từ MySQL theo session_id """
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT role, message FROM chats WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
        chat_logs = await cursor.fetchall()
    await conn.ensure_closed()
    return [{"role": log[0], "content": log[1]} for log in chat_logs]

async def chat_with_mie(prompt: str, session_id: str, api_key: str) -> str:
    """ Xử lý hội thoại với chatbot Mie-san """
    if not await verify_api_key(api_key):
        return "API Key không hợp lệ!"

    chat_history = await get_chat_history(session_id)
   ## related_info = await search_faiss(prompt)

    messages = [{"role": "system", "content": "Bạn là một trợ lý AI thông minh."}]
    if chat_history:
        messages.extend(chat_history)

    user_message = {"role": "user", "content": prompt}
  ##  if related_info:
   ##     user_message["content"] += f"\nThông tin liên quan: {related_info}"
    messages.append(user_message)

    response = client_ollama.chat.completions.create(
        model="gemma2:2b",
        messages=messages
    )

    return response.choices[0].message.content
