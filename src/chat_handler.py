import os
from openai import OpenAI
from src.faiss_index import search_faiss
from src.database import get_chat_history, verify_api_key
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API Ollama từ biến môi trường
API_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("OLLAMA_API_KEY", "duogxaolin")

# Khởi tạo client OpenAI (tương thích với Ollama)
client_ollama = OpenAI(
    base_url=API_URL,
    api_key=API_KEY
)

def chat_with_mie(prompt: str, session_id: str, api_key: str) -> str:
    """
    Xử lý hội thoại với chatbot Mie-san
    - Kiểm tra API key hợp lệ
    - Lấy lịch sử chat từ MongoDB
    - Tìm kiếm dữ liệu liên quan từ FAISS
    - Gửi truy vấn lên Ollama

    Args:
        prompt (str): Nội dung câu hỏi của người dùng
        session_id (str): ID phiên làm việc
        api_key (str): API key xác thực người dùng

    Returns:
        str: Câu trả lời từ AI hoặc thông báo lỗi
    """

    # ✅ Kiểm tra API Key hợp lệ
    if not verify_api_key(api_key):
        return "API Key không hợp lệ!"

    # ✅ Lấy lịch sử chat từ MongoDB
    chat_history = get_chat_history(session_id)

    # ✅ Tìm kiếm dữ liệu liên quan với FAISS
    related_info = search_faiss(prompt)

    # ✅ Chuẩn bị danh sách tin nhắn gửi đi
    messages = [{"role": "system", "content": "Bạn là một trợ lý AI thông minh."}]

    # Thêm lịch sử chat nếu có
    if chat_history:
        messages.extend(chat_history)

    # Tạo tin nhắn người dùng, bổ sung thông tin từ FAISS nếu có
    user_message = {"role": "user", "content": prompt}
    if related_info:
        user_message["content"] += f"\nThông tin liên quan: {related_info}"

    messages.append(user_message)

    # ✅ Gửi truy vấn đến Ollama
    response = client_ollama.chat.completions.create(
        model="gemma:2b",
        messages=messages
    )

    return response.choices[0].message.content
