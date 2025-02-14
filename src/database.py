import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self, host: str, user: str, password: str, db: str, autocommit: bool = True):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.autocommit = autocommit
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            autocommit=self.autocommit
        )
        print("✅ Connected to MySQL database.")

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("❌ Database connection closed.")

# Global instance của DatabaseManager
db_manager = DatabaseManager(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    db=os.getenv("MYSQL_DATABASE", "mie_san")
)

async def create_database():
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    db = os.getenv("MYSQL_DATABASE", "mie_san")
    conn = await aiomysql.connect(host=host, user=user, password=password)
    async with conn.cursor() as cursor:
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
    conn.close()

async def create_tables():
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    db = os.getenv("MYSQL_DATABASE", "mie_san")
    conn = await aiomysql.connect(host=host, user=user, password=password, db=db)
    async with conn.cursor() as cursor:
        # Bảng users
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            api_key VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Bảng chats
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
        # Bảng files
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            filepath VARCHAR(255) NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    conn.close()

async def init_db():
    await create_database()
    await create_tables()
    await db_manager.connect()

async def close_db():
    await db_manager.close()
