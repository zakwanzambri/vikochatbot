"""
Plain text file extraction
"""
from pathlib import Path
from typing import Dict
import chardet


class TextExtractor:
    """Extract text from plain text files"""
    
    def __init__(self):
        self.supported_extension = '.txt'
    
    def extract_text(self, file_path: str) -> Dict[str, any]:
        """
        Extract text from a TXT file
        
        Args:
            file_path: Path to the TXT file
            
        Returns:
            Dictionary containing:
                - text: Extracted text
                - encoding: Detected encoding
                - filename: Original filename
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() != self.supported_extension:
            raise ValueError(f"Invalid file type. Expected {self.supported_extension}, got {path.suffix}")
        
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] or 'utf-8'
            
            # Read text with detected encoding
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                text = f.read()
            
            return {
                'text': text,
                'encoding': encoding,
                'filename': path.name,
                'file_type': 'txt'
            }
            
        except Exception as e:
            raise Exception(f"Error extracting text from TXT file: {str(e)}")
