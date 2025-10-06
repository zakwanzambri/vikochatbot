"""
Document retrieval system
"""
from typing import List, Dict
from src.embedding.embedder import OpenAIEmbedder
from src.vector_store.faiss_store import FAISSVectorStore
from src.vector_store.chroma_store import ChromaVectorStore
from src.config import TOP_K_RESULTS, VECTOR_STORE_TYPE


class DocumentRetriever:
    """Retrieve relevant document chunks based on queries"""
    
    def __init__(self, vector_store, embedder: OpenAIEmbedder = None, top_k: int = None):
        """
        Initialize the retriever
        
        Args:
            vector_store: Vector store instance (FAISS or ChromaDB)
            embedder: Embedder instance for query embedding
            top_k: Number of results to retrieve
        """
        self.vector_store = vector_store
        self.embedder = embedder or OpenAIEmbedder()
        self.top_k = top_k or TOP_K_RESULTS
    
    def retrieve(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of results to return (overrides default)
            
        Returns:
            List of relevant document chunks with scores
        """
        if not query or not query.strip():
            return []
        
        k = top_k or self.top_k
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=k)
        
        return results
    
    def retrieve_with_threshold(self, query: str, threshold: float = 0.7, top_k: int = None) -> List[Dict]:
        """
        Retrieve relevant documents with a minimum similarity threshold
        
        Args:
            query: Search query
            threshold: Minimum similarity score (0-1)
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks above the threshold
        """
        results = self.retrieve(query, top_k)
        
        # Filter by threshold
        filtered_results = [r for r in results if r.get('score', 0) >= threshold]
        
        return filtered_results
    
    def format_context(self, results: List[Dict], max_length: int = 4000) -> str:
        """
        Format retrieved documents into a context string
        
        Args:
            results: List of retrieved document chunks
            max_length: Maximum length of context in characters
            
        Returns:
            Formatted context string
        """
        if not results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for i, result in enumerate(results, 1):
            text = result.get('text', '')
            filename = result.get('filename', 'Unknown')
            score = result.get('score', 0)
            
            # Format chunk with metadata
            chunk_text = f"[Source {i}: {filename} (relevance: {score:.2f})]\n{text}\n"
            
            # Check if adding this chunk would exceed max length
            if current_length + len(chunk_text) > max_length:
                # Try to add at least part of it
                remaining = max_length - current_length
                if remaining > 100:  # Only add if there's reasonable space
                    chunk_text = chunk_text[:remaining] + "...\n"
                    context_parts.append(chunk_text)
                break
            
            context_parts.append(chunk_text)
            current_length += len(chunk_text)
        
        return "\n".join(context_parts)
    
    def get_relevant_sources(self, results: List[Dict]) -> List[str]:
        """
        Extract unique source filenames from results
        
        Args:
            results: List of retrieved document chunks
            
        Returns:
            List of unique source filenames
        """
        sources = set()
        for result in results:
            filename = result.get('filename')
            if filename:
                sources.add(filename)
        
        return sorted(list(sources))
