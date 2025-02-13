import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mie_san_db")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

pdf_collection = db["pdf_data"]
excel_collection = db["excel_data"]
