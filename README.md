# Mie-san: AI Chatbot with Ollama & MySQL

Mie-san is an AI chatbot that integrates **Ollama** with **MySQL** for storing and retrieving data from PDF/Excel files. It also utilizes **FAISS** for intelligent searching.

## 🌟 Features
- 🤖 **Chatbot** (via **Ollama**)  
- 📄 **Upload & Extract** data from **PDF / Excel**  
- 🔎 **Smart Searching** with **FAISS + MySQL**  

## 🚀 Tech Stack
- **FastAPI** – API framework  
- **MySQL** – Database  
- **FAISS** – Fast Similarity Search  
- **Ollama** – AI Model Execution  
- **OpenAI API** (Self-hosted)  

## 📦 Installation
```bash
git clone https://github.com/duogxaolin/mie-san.git
cd mie-san
```

## Usage
```bash
pip install -r requirements.txt

#python main.py
uvicorn main:app --reload

```

## Cấu trúc
```bash
mie-san/
│── .env                   # Config database
│── .gitignore             # Chặn file .env khỏi Git
│── main.py                # Chỉ chứa router
│── requirements.txt        # Thư viện cần cài đặt
│── uploads/               # Lưu file PDF, Excel
│── src/
│   ├── database.py        # Kết nối MySQL
│   ├── repositories.py    # Quản lý kết nối OOP
│   ├── faiss_index.py     # Xử lý FAISS
│   ├── process_pdf.py     # Xử lý PDF
│   ├── process_excel.py   # Xử lý Excel
│   ├── chat_handler.py    # Chatbot Mie-san
│   ├── routes/
│   │   ├── upload.py  # API upload PDF, Excel 
│   │   ├── chat.py    # API chat  
```
