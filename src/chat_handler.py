import os
import redis
from openai import OpenAI
from src.faiss_index import search_faiss
from src.database import get_chat_history, verify_api_key, update_api_usage
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("OLLAMA_URL")
API_KEY = os.getenv("OLLAMA_API_KEY")

client_ollama = OpenAI(base_url=API_URL, api_key=API_KEY)

# Redis cache
cache = redis.Redis(host='localhost', port=6379, db=0)

def chat_with_mie(prompt: str, session_id: str, api_key: str) -> str:
    if not verify_api_key(api_key):
        return "API Key không hợp lệ!"

    update_api_usage(api_key)

    cache_key = f"chat:{session_id}:{prompt}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response.decode("utf-8")

    chat_history = get_chat_history(session_id)
    related_info = search_faiss(prompt)

    messages = [{"role": "system", "content": "Bạn là một trợ lý AI thông minh."}]
    if chat_history:
        messages.extend(chat_history)

    user_message = {"role": "user", "content": prompt}
    if related_info:
        user_message["content"] += f"\nThông tin liên quan: {related_info}"
    messages.append(user_message)

    response = client_ollama.chat.completions.create(
        model="gemma:2b",
        messages=messages
    )

    reply = response.choices[0].message.content
    cache.setex(cache_key, 300, reply)
    return reply
