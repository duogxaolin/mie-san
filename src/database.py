from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mie_san_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
users_collection = db["users"]
chats_collection = db["chats"]
pdf_collection = db["pdf_data"]
excel_collection = db["excel_data"]
def verify_api_key(api_key):
    """ Kiểm tra API key có tồn tại trong MongoDB không """
    return users_collection.find_one({"api_key": api_key}) is not None

def get_chat_history(session_id):
    """ Lấy lịch sử chat từ MongoDB theo session_id """
    chat_logs = chats_collection.find({"session_id": session_id}).sort("timestamp", 1)
    return [{"role": log["role"], "content": log["message"]} for log in chat_logs]
