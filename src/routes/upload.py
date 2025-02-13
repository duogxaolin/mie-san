from fastapi import APIRouter, UploadFile, File
from src.process_pdf import save_pdf_to_mongo
from src.process_excel import save_excel_to_mongo
import shutil

router = APIRouter()

@router.post("/upload/pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": save_pdf_to_mongo(file_path)}

@router.post("/upload/excel/")
async def upload_excel(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": save_excel_to_mongo(file_path)}
