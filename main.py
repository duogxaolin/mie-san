from fastapi import FastAPI
from dotenv import load_dotenv
import os

from src.database import init_db, close_db
from src.routes.upload import router as upload_router
from src.routes.chat import router as chat_router

load_dotenv()
PORT = os.getenv("PORT", "8080")
HOST_URL = os.getenv("HOST_URL", "127.0.0.1")

app = FastAPI(
    title="Mie-san API",
    description="API for AI chatbot with MySQL support",
    version="1.0.1"
)

@app.on_event("startup")
async def startup_event():
    await init_db()  # Khởi tạo database, tạo bảng và thiết lập connection pool

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()  # Đóng connection pool khi server dừng

app.include_router(upload_router)
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=int(PORT))
