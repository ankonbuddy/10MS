import os
import PyPDF2
import re
from typing import List

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def clean_text(text: str) -> str:
    # Remove non-printable characters, normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F\u0980-\u09FF ]+', '', text)  # Keep English and Bengali
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def load_and_chunk_pdfs(pdf_dir: str) -> List[str]:
    all_chunks = []
    for fname in os.listdir(pdf_dir):
        if fname.lower().endswith('.pdf'):
            raw = extract_text_from_pdf(os.path.join(pdf_dir, fname))
            cleaned = clean_text(raw)
            chunks = chunk_text(cleaned)
            all_chunks.extend(chunks)
    return all_chunks 