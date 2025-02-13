import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.database import pdf_collection, excel_collection

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def build_faiss_index():
    """
    Xây dựng FAISS Index từ dữ liệu MongoDB.
    """
    data = list(pdf_collection.find({}, {"_id": 0, "content": 1})) + \
           list(excel_collection.find({}, {"_id": 0, "content": 1}))

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
    """
    Tìm kiếm dữ liệu liên quan từ FAISS.
    """
    try:
        index = faiss.read_index("faiss_index.bin")
    except:
        return "Không tìm thấy dữ liệu."

    query_vector = model.encode([query])
    _, indices = index.search(np.array(query_vector), 1)

    data = list(pdf_collection.find({}, {"_id": 0, "content": 1})) + \
           list(excel_collection.find({}, {"_id": 0, "content": 1}))

    return data[indices[0][0]]["content"]
