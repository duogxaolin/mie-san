import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Kết nối MySQL
db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)
cursor = db.cursor(dictionary=True)

def verify_api_key(api_key):
    """ Kiểm tra API key hợp lệ """
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE api_key = %s", (api_key,))
    return cursor.fetchone()["count"] > 0

def get_chat_history(session_id):
    """ Lấy lịch sử chat từ MySQL """
    cursor.execute("SELECT role, message FROM chat_history WHERE session_id = %s ORDER BY timestamp ASC", (session_id,))
    return cursor.fetchall()

def update_api_usage(api_key):
    """ Giới hạn API sử dụng """
    cursor.execute("UPDATE users SET request_count = request_count + 1 WHERE api_key = %s", (api_key,))
    db.commit()
