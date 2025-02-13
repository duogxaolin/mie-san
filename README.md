# Mie-san: AI Chatbot with Ollama & MongoDB

Mie-san is an AI chatbot that integrates **Ollama** with **MongoDB** for storing and retrieving data from PDF/Excel files. It also utilizes **FAISS** for intelligent searching.

## 🌟 Features
- 🤖 **Chatbot** (via **Ollama**)  
- 📄 **Upload & Extract** data from **PDF / Excel**  
- 🔎 **Smart Searching** with **FAISS + MongoDB**  

## 🚀 Tech Stack
- **FastAPI** – API framework  
- **MongoDB** – Database  
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
python -m pip install -r requirements.txt

#python main.py
uvicorn main:app --reload

```
