import pandas as pd
from src.database import db_manager
from src.faiss_index import build_faiss_index
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def read_excel(excel_path: str):
    loop = asyncio.get_event_loop()
    def _read():
        return pd.read_excel(excel_path)
    df = await loop.run_in_executor(executor, _read)
    return df

async def save_excel_to_mysql(excel_path: str) -> str:
    df = await read_excel(excel_path)
    text = "\n".join(df.astype(str).values.flatten())
    pool = db_manager.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO excel_data (content) VALUES (%s)", (text,))
    asyncio.create_task(build_faiss_index())
    return "Excel đã được lưu vào MySQL."
