# Multilingual RAG Pipeline (English & Bengali)

This project implements a basic Retrieval-Augmented Generation (RAG) system using Ollama, FastAPI, and a PDF document corpus. It supports both English and Bengali queries.

## Features
- Accepts user queries in English and Bengali
- Retrieves relevant document chunks from a PDF knowledge base
- Generates answers grounded in retrieved content using Ollama LLM
- Maintains short-term (chat history) and long-term (vector DB) memory
- REST API for chat and PDF upload

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama:**
   - Download and run Ollama from [https://ollama.com/](https://ollama.com/)
   - Pull a model (e.g., llama3):
     ```bash
     ollama pull llama3
     ```
   - Ensure Ollama is running on `http://localhost:11434`

3. **Add your PDF files:**
   - Place PDF files in `data/corpus/`

4. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Usage

### `/chat` (POST)
- **Request:**
  ```json
  { "query": "Your question here (English or Bengali)" }
  ```
- **Response:**
  ```json
  { "answer": "Model-generated answer" }
  ```

### `/upload_pdf` (POST)
- Upload a new PDF to the corpus and update the index.

## Evaluation
- The system retrieves top-k relevant chunks using cosine similarity (FAISS).
- Answers are grounded in retrieved context.
- For further evaluation, inspect the retrieved context and model output.

---

**Note:** This is a basic RAG pipeline. For production, consider persistent vector DB, better chunking, and advanced evaluation metrics. 