from fastapi import FastAPI
import os
from src.routes.upload import router as upload_router
from src.routes.chat import router as chat_router
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", "8080")
HOST_URL = os.getenv("HOST_URL", "127.0.0.1")

app = FastAPI(
    title="Mie-san API",
    description="API for AI chatbot with PDF/Excel support",
    version="1.0.0"
)


app.include_router(upload_router)
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=PORT)
