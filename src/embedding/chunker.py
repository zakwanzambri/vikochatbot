"""
Text chunking for document processing
"""
from typing import List, Dict
import re


class TextChunker:
    """Split text into manageable chunks for embedding"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        if not text or not text.strip():
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            # Calculate end position
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to break at a sentence or word boundary
            if end < len(text):
                # Try to find a sentence boundary (., !, ?)
                sentence_end = self._find_sentence_boundary(text, start, end)
                if sentence_end > start:
                    end = sentence_end
                else:
                    # Try to find a word boundary
                    word_end = self._find_word_boundary(text, start, end)
                    if word_end > start:
                        end = word_end
            
            # Extract chunk
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk_data = {
                    'text': chunk_text,
                    'chunk_id': chunk_id,
                    'start_pos': start,
                    'end_pos': end
                }
                
                # Add metadata if provided
                if metadata:
                    chunk_data.update(metadata)
                
                chunks.append(chunk_data)
                chunk_id += 1
            
            # Move start position (with overlap)
            start = end - self.chunk_overlap
            
            # Ensure we make progress
            if start <= chunks[-1]['start_pos'] if chunks else 0:
                start = end
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """Find the nearest sentence boundary before the end position"""
        # Look for sentence endings in the last 200 characters
        search_start = max(start, end - 200)
        search_text = text[search_start:end]
        
        # Find the last occurrence of sentence-ending punctuation
        for i in range(len(search_text) - 1, -1, -1):
            if search_text[i] in '.!?' and (i + 1 >= len(search_text) or search_text[i + 1].isspace()):
                return search_start + i + 1
        
        return -1
    
    def _find_word_boundary(self, text: str, start: int, end: int) -> int:
        """Find the nearest word boundary before the end position"""
        # Look back from end to find a space
        for i in range(end - 1, start, -1):
            if text[i].isspace():
                return i + 1
        
        return -1
    
    def chunk_by_paragraphs(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text by paragraphs, then further chunk if paragraphs are too large
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        paragraphs = text.split('\n\n')
        chunks = []
        chunk_id = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # If paragraph is small enough, use it as a chunk
            if len(para) <= self.chunk_size:
                chunk_data = {
                    'text': para,
                    'chunk_id': chunk_id,
                }
                if metadata:
                    chunk_data.update(metadata)
                chunks.append(chunk_data)
                chunk_id += 1
            else:
                # If paragraph is too large, split it further
                sub_chunks = self.chunk_text(para, metadata)
                for sub_chunk in sub_chunks:
                    sub_chunk['chunk_id'] = chunk_id
                    chunks.append(sub_chunk)
                    chunk_id += 1
        
        return chunks
