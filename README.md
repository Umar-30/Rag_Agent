# RAG Insight Assistant

A professional, high-end Retrieval-Augmented Generation (RAG) application built with **FastAPI**, **Streamlit**, **Cohere**, and **Qdrant**.

## 🚀 Features
- **Modern AI UI**: Unified landing page and chat interface with a premium dark theme.
- **Neural Search**: Efficient document retrieval using Qdrant vector database.
- **SaaS Styling**: Glassmorphism effects, neon borders, and optimized for laptop screens.
- **Dynamic Ingestion**: Process PDFs into vector embeddings on the fly.
- **Scalable Backend**: FastAPI-powered engine for query synthesis and generation.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM & Embeddings**: Cohere
- **Vector DB**: Qdrant
- **Dependency Management**: uv

## 📦 Setup & Running

### 1. Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) installed
- [Qdrant](https://qdrant.tech/) running locally on port 6333

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
```

### 3. Run the Backend
```bash
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Run the Frontend
```bash
uv run streamlit run ui.py
```

## 🐳 Docker Deployment
The project includes a `Dockerfile` for containerized deployment.
```bash
docker build -t rag-assistant .
docker run -p 8000:8000 -p 7860:7860 rag-assistant
```

---
*Powered by Cohere and Qdrant • Developed for RAG Insights*
