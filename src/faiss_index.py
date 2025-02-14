import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.database import get_db_connection
import asyncio

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def fetch_data_from_mysql():
    """ Lấy nội dung PDF và Excel từ MySQL """
    conn = await get_db_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT content FROM pdf_data")
        pdf_data = await cursor.fetchall()

        await cursor.execute("SELECT content FROM excel_data")
        excel_data = await cursor.fetchall()

    await conn.ensure_closed()
    return [row[0] for row in pdf_data] + [row[0] for row in excel_data]

async def build_faiss_index():
    """ Xây dựng FAISS Index từ MySQL """
    data = await fetch_data_from_mysql()
    if not data:
        return None

    embeddings = model.encode(data)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, "faiss_index.bin")
    return index

async def search_faiss(query):
    """ Tìm kiếm dữ liệu liên quan từ FAISS """
    try:
        index = faiss.read_index("faiss_index.bin")
    except:
        return "Không tìm thấy dữ liệu."

    query_vector = model.encode([query])
    _, indices = index.search(np.array(query_vector), 1)

    data = await fetch_data_from_mysql()
    return data[indices[0][0]] if indices[0][0] < len(data) else "Không có kết quả."
