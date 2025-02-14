from typing import List, Dict, Any

class BaseRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    async def execute_query(self, query: str, params: tuple = None) -> List[Any]:
        pool = self.db_manager.pool
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                result = await cursor.fetchall()
        return result

    async def execute_command(self, query: str, params: tuple = None):
        pool = self.db_manager.pool
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)

class UserRepository(BaseRepository):
    async def get_user_by_api_key(self, api_key: str) -> Dict[str, Any]:
        query = "SELECT id, username, password, api_key, created_at FROM users WHERE api_key = %s LIMIT 1"
        result = await self.execute_query(query, (api_key,))
        if result:
            row = result[0]
            return {
                "id": row[0],
                "username": row[1],
                "password": row[2],
                "api_key": row[3],
                "created_at": row[4]
            }
        return {}

class ChatRepository(BaseRepository):
    async def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        query = "SELECT role, message FROM chats WHERE session_id = %s ORDER BY timestamp ASC"
        results = await self.execute_query(query, (session_id,))
        return [{"role": row[0], "message": row[1]} for row in results]

    async def add_chat(self, user_id: int, message: str, session_id: str, response: str):
        query = "INSERT INTO chats (user_id, message, session_id, response) VALUES (%s, %s, %s, %s)"
        await self.execute_command(query, (user_id, message, session_id, response))

class FileRepository(BaseRepository):
    async def add_file(self, filename: str, filepath: str):
        query = "INSERT INTO files (filename, filepath) VALUES (%s, %s)"
        await self.execute_command(query, (filename, filepath))
