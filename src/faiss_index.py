import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.database import cursor

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_faiss_index():
    cursor.execute("SELECT content FROM pdf_data UNION SELECT content FROM excel_data")
    data = cursor.fetchall()

    if not data:
        return None

    texts = [item["content"] for item in data]
    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, "faiss_index.bin")
    return index

def search_faiss(query):
    try:
        index = faiss.read_index("faiss_index.bin")
    except:
        return "Không tìm thấy dữ liệu."

    query_vector = model.encode([query])
    _, indices = index.search(np.array(query_vector), 1)

    cursor.execute("SELECT content FROM pdf_data UNION SELECT content FROM excel_data")
    data = cursor.fetchall()

    return data[indices[0][0]]["content"]
