from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple

class VectorStore:
    def __init__(self, model_name: str = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.text_chunks = []

    def build_index(self, chunks: List[str]):
        self.text_chunks = chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def query(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        query_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_emb, top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx < len(self.text_chunks):
                results.append((self.text_chunks[idx], float(dist)))
        return results 