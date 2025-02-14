from fastapi import APIRouter, UploadFile, File
from src.process_pdf import save_pdf_to_mysql
from src.process_excel import save_excel_to_mysql
import shutil
import os

router = APIRouter()

@router.post("/upload/pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = await save_pdf_to_mysql(file_path)
    os.remove(file_path)  # Xoá file sau khi xử lý
    return {"message": result}

@router.post("/upload/excel/")
async def upload_excel(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = await save_excel_to_mysql(file_path)
    os.remove(file_path)
    return {"message": result}
