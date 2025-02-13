import pdfplumber
from src.database import pdf_collection
from src.faiss_index import build_faiss_index

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text.strip()

def save_pdf_to_mongo(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    pdf_collection.insert_one({"type": "pdf", "content": text})
    build_faiss_index()
    return "PDF đã được lưu vào MongoDB."
