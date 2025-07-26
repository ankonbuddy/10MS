import httpx
from typing import List
from .vector_store import VectorStore
from .memory import ShortTermMemory

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama endpoint
OLLAMA_MODEL = "llama3"  # Change to your preferred model

class RAGPipeline:
    def __init__(self, vector_store: VectorStore, memory: ShortTermMemory):
        self.vector_store = vector_store
        self.memory = memory

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        results = self.vector_store.query(query, top_k=top_k)
        return [chunk for chunk, _ in results]

    def generate(self, query: str, context: List[str], history: List[dict]) -> str:
        # Compose prompt with context and chat history
        prompt = "You are a helpful assistant. Use the following context to answer the user's question.\n"
        if history:
            prompt += "\nChat history:\n"
            for turn in history:
                prompt += f"{turn['user']}: {turn['message']}\n"
        prompt += "\nContext:\n"
        for i, chunk in enumerate(context):
            prompt += f"[{i+1}] {chunk}\n"
        prompt += f"\nUser: {query}\nAssistant:"
        # Call Ollama
        response = httpx.post(OLLAMA_API_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    def chat(self, user_query: str) -> str:
        self.memory.add("User", user_query)
        context = self.retrieve(user_query)
        history = self.memory.get_history()
        answer = self.generate(user_query, context, history)
        self.memory.add("Assistant", answer)
        return answer 