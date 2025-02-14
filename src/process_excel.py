import pandas as pd
from src.database import get_db_connection
from src.faiss_index import build_faiss_index
import asyncio

async def save_excel_to_mysql(excel_path):
    """ Lưu Excel vào MySQL """
    df = pd.read_excel(excel_path)
    text = "\n".join(df.astype(str).values.flatten())

    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO excel_data (content) VALUES (%s)", (text,))
        await conn.commit()
    await conn.ensure_closed()

    await build_faiss_index()
    return "Excel đã được lưu vào MySQL."
