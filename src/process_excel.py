import pandas as pd
from src.database import excel_collection
from src.faiss_index import build_faiss_index

def save_excel_to_mongo(excel_path):
    df = pd.read_excel(excel_path)
    text = "\n".join(df.astype(str).values.flatten())

    excel_collection.insert_one({"type": "excel", "content": text})
    build_faiss_index()
    return "Excel đã được lưu vào MongoDB."
