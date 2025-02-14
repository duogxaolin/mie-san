import aiomysql
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DATABASE", "mie_san")

pool = None  # Connection pool

async def create_database():
    """Tạo database nếu chưa có"""
    conn = await aiomysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )
    async with conn.cursor() as cursor:
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    await conn.ensure_closed()

async def create_tables():
    """Tạo các bảng cần thiết nếu chưa có"""
    conn = await aiomysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB
    )
    async with conn.cursor() as cursor:
        # Tạo bảng users
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            api_key VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tạo bảng chats
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            message TEXT NOT NULL,
            session_id VARCHAR(255) NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # Tạo bảng files
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            filepath VARCHAR(255) NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
    await conn.ensure_closed()

async def connect_to_db():
    """Kết nối MySQL và tạo connection pool"""
    global pool
    await create_database()  # Tạo database nếu chưa có
    await create_tables()  # Tạo bảng nếu chưa có
    pool = await aiomysql.create_pool(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        autocommit=True
    )
    print("✅ Đã kết nối MySQL và thiết lập database!")

async def close_db():
    """Đóng connection pool khi tắt server"""
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()
        print("❌ Đã đóng kết nối MySQL.")

async def get_db_connection():
    """Lấy kết nối từ pool"""
    global pool
    if not pool:
        await connect_to_db()
    return await pool.acquire()
