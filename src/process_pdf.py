import pdfplumber
from src.database import cursor, db
from src.faiss_index import build_faiss_index

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()]).strip()

def save_pdf_to_mysql(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    cursor.execute("INSERT INTO pdf_data (content) VALUES (%s)", (text,))
    db.commit()
    build_faiss_index()
    return "PDF đã được lưu vào MySQL."
