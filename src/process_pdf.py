import pdfplumber
from src.database import db_manager
from src.faiss_index import build_faiss_index
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def extract_text_from_pdf(pdf_path: str) -> str:
    loop = asyncio.get_event_loop()
    def _extract():
        with pdfplumber.open(pdf_path) as pdf:
            texts = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "\n".join(texts)
    text = await loop.run_in_executor(executor, _extract)
    return text.strip()

async def save_pdf_to_mysql(pdf_path: str) -> str:
    text = await extract_text_from_pdf(pdf_path)
    pool = db_manager.pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO pdf_data (content) VALUES (%s)", (text,))
    # Chạy rebuild FAISS index dưới background (nếu cần)
    asyncio.create_task(build_faiss_index())
    return "PDF đã được lưu vào MySQL."
