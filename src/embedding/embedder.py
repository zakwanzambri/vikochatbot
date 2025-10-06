"""
OpenAI Embeddings generation
"""
from openai import OpenAI
from typing import List, Dict
import numpy as np
from src.config import OPENAI_API_KEY, EMBEDDING_MODEL


class OpenAIEmbedder:
    """Generate embeddings using OpenAI's API"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the embedder
        
        Args:
            api_key: OpenAI API key (defaults to config)
            model: Embedding model to use (defaults to config)
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or EMBEDDING_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Filter out empty texts
        valid_texts = [t for t in texts if t and t.strip()]
        
        if not valid_texts:
            raise ValueError("No valid texts to embed")
        
        embeddings = []
        
        try:
            # Process in batches to avoid rate limits
            for i in range(0, len(valid_texts), batch_size):
                batch = valid_texts[i:i + batch_size]
                
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                
                # Extract embeddings in the correct order
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except Exception as e:
            raise Exception(f"Error generating batch embeddings: {str(e)}")
    
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for a list of text chunks
        
        Args:
            chunks: List of chunk dictionaries (must contain 'text' key)
            
        Returns:
            List of chunks with added 'embedding' key
        """
        if not chunks:
            return []
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.embed_batch(texts)
        
        # Add embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding
        
        return chunks
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
