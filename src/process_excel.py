import pandas as pd
from src.database import cursor, db
from src.faiss_index import build_faiss_index

def save_excel_to_mysql(excel_path):
    """ Đọc file Excel, chuyển đổi thành text và lưu vào MySQL """
    df = pd.read_excel(excel_path, engine="openpyxl")
    text = "\n".join(df.astype(str).values.flatten())

    cursor.execute("INSERT INTO excel_data (content) VALUES (%s)", (text,))
    db.commit()
    
    build_faiss_index()
    return "Excel đã được lưu vào MySQL."
