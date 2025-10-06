"""
Ollama integration for local LLMs (FREE!)
"""
import requests
from typing import List, Dict
import json


class OllamaEmbedder:
    """Generate embeddings using local Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "nomic-embed-text"):
        """
        Initialize Ollama embedder
        
        Args:
            base_url: Ollama API URL
            model: Embedding model (nomic-embed-text, mxbai-embed-large)
        """
        self.base_url = base_url
        self.model = model
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model, "prompt": text}
        )
        return response.json()['embedding']
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Generate embeddings for text chunks"""
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embed_batch(texts)
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding
        
        return chunks


class OllamaChat:
    """Chat completion using local Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        """
        Initialize Ollama chat
        
        Args:
            base_url: Ollama API URL
            model: Model name (llama3.1, mistral, phi3, etc.)
        """
        self.base_url = base_url
        self.model = model
        
        self.system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.

IMPORTANT RULES:
1. Answer questions ONLY using information from the provided context/documents
2. If the answer is not in the documents, respond with: "⚠️ I couldn't find that information in your documents."
3. Always cite which source document you're using when answering
4. Be concise and accurate
5. If you're not completely sure, acknowledge the uncertainty
6. Do not make up information or use external knowledge"""
    
    def chat(self, question: str, context: str = "") -> str:
        """Generate a response to a question with context"""
        
        if context:
            prompt = f"""{self.system_prompt}

Context from documents:
{context}

Question: {question}

Answer based on the context above:"""
        else:
            prompt = f"{self.system_prompt}\n\nQuestion: {question}\n\nNo context available."
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()['response']
        except Exception as e:
            return f"❌ Error: {str(e)}"
