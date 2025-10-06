"""
Google Gemini integration for embeddings and chat
"""
import google.generativeai as genai
from typing import List, Dict
import os


class GeminiEmbedder:
    """Generate embeddings using Google's Gemini API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini embedder
        
        Args:
            api_key: Google API key
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        genai.configure(api_key=self.api_key)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    
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


class GeminiChat:
    """Chat completion using Google's Gemini"""
    
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        """
        Initialize Gemini chat
        
        Args:
            api_key: Google API key
            model: Model name (gemini-1.5-flash or gemini-1.5-pro)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        
        self.system_prompt = """You are a helpful AI assistant that answers questions based on provided documents.

IMPORTANT RULES:
1. Answer questions ONLY using information from the provided context/documents
2. If the answer is not in the documents, respond with: "⚠️ I couldn't find that information in your documents."
3. Always cite which source document you're using when answering
4. Be concise and accurate
5. If you're not completely sure, acknowledge the uncertainty
6. Do not make up information or use external knowledge

When you find relevant information, format your answer clearly and mention the source."""
    
    def chat(self, question: str, context: str = "") -> str:
        """Generate a response to a question with context"""
        
        if context:
            prompt = f"""{self.system_prompt}

Context from documents:
{context}

Question: {question}

Please answer based on the context above."""
        else:
            prompt = f"""{self.system_prompt}

Question: {question}

No relevant context found. Please respond with: "⚠️ I couldn't find that information in your documents." """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error: {str(e)}"
