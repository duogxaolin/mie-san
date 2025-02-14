import pdfplumber
from src.database import get_db_connection
from src.faiss_index import build_faiss_index
import asyncio

async def extract_text_from_pdf(pdf_path):
    """ Trích xuất văn bản từ PDF """
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text.strip()

async def save_pdf_to_mysql(pdf_path):
    """ Lưu PDF vào MySQL """
    text = await extract_text_from_pdf(pdf_path)
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("INSERT INTO pdf_data (content) VALUES (%s)", (text,))
        await conn.commit()
    await conn.ensure_closed()
    await build_faiss_index()
    return "PDF đã được lưu vào MySQL."
