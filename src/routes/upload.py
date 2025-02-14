from fastapi import APIRouter, UploadFile, File
from src.process_pdf import save_pdf_to_mysql
from src.process_excel import save_excel_to_mysql
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """ Xử lý upload PDF """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = save_pdf_to_mysql(file_path)
    os.remove(file_path)  # Xóa file sau khi xử lý

    return {"message": result}

@router.post("/upload/excel/")
async def upload_excel(file: UploadFile = File(...)):
    """ Xử lý upload Excel """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = save_excel_to_mysql(file_path)
    os.remove(file_path)  # Xóa file sau khi xử lý

    return {"message": result}
