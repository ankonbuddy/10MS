from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.pdf_utils import load_and_chunk_pdfs
from app.vector_store import VectorStore
from app.memory import ShortTermMemory
from app.rag import RAGPipeline
import os

app = FastAPI()

# Load and index the PDF corpus at startup
PDF_DIR = os.path.join(os.path.dirname(__file__), '../data/corpus')  
chunks = load_and_chunk_pdfs(PDF_DIR)
vector_store = VectorStore()
vector_store.build_index(chunks)
memory = ShortTermMemory(max_turns=5)
rag_pipeline = RAGPipeline(vector_store, memory)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    answer = rag_pipeline.chat(request.query)
    return ChatResponse(answer=answer)

# Optional: Endpoint to upload new PDFs and update the index
def update_index():
    global chunks, vector_store
    chunks = load_and_chunk_pdfs(PDF_DIR)
    vector_store.build_index(chunks)

@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...)):
    file_location = os.path.join(PDF_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    update_index()
    return {"status": "PDF uploaded and index updated."}